#!/usr/bin/env python3
"""
Investment Portfolio Tracker - Python Backend Server
No frameworks used - pure Python HTTP server
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request
import urllib.error
import ssl
import os
from datetime import datetime

# API Configuration - Replace with your actual API keys
ALPHA_VANTAGE_KEY = os.environ.get('Your Alpha Vantage API Key Here')
NEWS_API_KEY = os.environ.get('Your News API Key Here')

# Create SSL context for HTTPS requests
ssl_context = ssl.create_default_context()


class PortfolioHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set HTTP response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self._set_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # Route: Get stock data
            if path.startswith('/api/stock/'):
                symbol = path.split('/')[-1].upper()
                data = self.get_stock_data(symbol)
                self._set_headers()
                self.wfile.write(json.dumps(data).encode())
            
            # Route: Get crypto data
            elif path.startswith('/api/crypto/'):
                symbol = path.split('/')[-1].upper()
                data = self.get_crypto_data(symbol)
                self._set_headers()
                self.wfile.write(json.dumps(data).encode())
            
            # Route: Get financial news
            elif path == '/api/news':
                data = self.get_financial_news()
                self._set_headers()
                self.wfile.write(json.dumps(data).encode())
            
            # Route: Serve index.html
            elif path == '/' or path == '/index.html':
                self._set_headers(content_type='text/html')
                with open('index.html', 'rb') as f:
                    self.wfile.write(f.read())
            
            # Route: Serve CSS files
            elif path.endswith('.css'):
                try:
                    filename = path.lstrip('/')
                    self._set_headers(content_type='text/css')
                    with open(filename, 'rb') as f:
                        self.wfile.write(f.read())
                except FileNotFoundError:
                    self._set_headers(404)
                    self.wfile.write(b'/* CSS file not found */')
            
            # Route: Serve JavaScript files
            elif path.endswith('.js'):
                try:
                    filename = path.lstrip('/')
                    self._set_headers(content_type='application/javascript')
                    with open(filename, 'rb') as f:
                        self.wfile.write(f.read())
                except FileNotFoundError:
                    self._set_headers(404)
                    self.wfile.write(b'// JavaScript file not found')
            
            # Route: Handle favicon (prevent 404 errors)
            elif path == '/favicon.ico':
                self._set_headers(404)
                self.wfile.write(b'')
            
            # 404 Not Found
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not Found'}).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def get_stock_data(self, symbol):
        """Fetch stock data from Alpha Vantage API"""
        try:
            # Alpha Vantage Global Quote endpoint
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}'
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
            
            # Check if API returned data
            if 'Global Quote' not in data or not data['Global Quote']:
                return {'error': f'Stock symbol {symbol} not found or API limit reached'}
            
            quote = data['Global Quote']
            
            # Extract relevant information
            return {
                'symbol': symbol,
                'name': symbol,  # Alpha Vantage doesn't provide company name in this endpoint
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%').replace('%', ''),
                'volume': int(quote.get('06. volume', 0)),
                'timestamp': quote.get('07. latest trading day', '')
            }
        
        except urllib.error.HTTPError as e:
            return {'error': f'HTTP Error: {e.code}'}
        except urllib.error.URLError as e:
            return {'error': f'URL Error: {str(e)}'}
        except Exception as e:
            return {'error': f'Error fetching stock data: {str(e)}'}
    
    def get_crypto_data(self, symbol):
        """Fetch cryptocurrency data from CoinGecko API"""
        try:
            # Map common symbols to CoinGecko IDs
            crypto_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'USDT': 'tether',
                'BNB': 'binancecoin',
                'SOL': 'solana',
                'XRP': 'ripple',
                'ADA': 'cardano',
                'DOGE': 'dogecoin',
                'DOT': 'polkadot',
                'MATIC': 'matic-network',
                'LTC': 'litecoin',
                'LINK': 'chainlink',
                'UNI': 'uniswap',
                'AVAX': 'avalanche-2',
                'ATOM': 'cosmos'
            }
            
            crypto_id = crypto_map.get(symbol, symbol.lower())
            
            # CoinGecko API endpoint (no API key required for basic usage)
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true'
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
            
            if crypto_id not in data:
                return {'error': f'Cryptocurrency {symbol} not found'}
            
            crypto_data = data[crypto_id]
            
            return {
                'symbol': symbol,
                'name': crypto_id.replace('-', ' ').title(),
                'current_price': float(crypto_data.get('usd', 0)),
                'change_24h': float(crypto_data.get('usd_24h_change', 0)),
                'volume_24h': float(crypto_data.get('usd_24h_vol', 0))
            }
        
        except urllib.error.HTTPError as e:
            return {'error': f'HTTP Error: {e.code}'}
        except urllib.error.URLError as e:
            return {'error': f'URL Error: {str(e)}'}
        except Exception as e:
            return {'error': f'Error fetching crypto data: {str(e)}'}
    
    def get_financial_news(self):
        """Fetch financial news from News API"""
        try:
            # News API endpoint for business news
            url = f'https://newsapi.org/v2/top-headlines?category=business&country=us&apiKey={NEWS_API_KEY}'
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
            
            if data.get('status') != 'ok':
                return {'error': 'Failed to fetch news', 'articles': []}
            
            return {
                'status': 'ok',
                'totalResults': data.get('totalResults', 0),
                'articles': data.get('articles', [])
            }
        
        except urllib.error.HTTPError as e:
            return {'error': f'HTTP Error: {e.code}', 'articles': []}
        except urllib.error.URLError as e:
            return {'error': f'URL Error: {str(e)}', 'articles': []}
        except Exception as e:
            return {'error': f'Error fetching news: {str(e)}', 'articles': []}
    
    def log_message(self, format, *args):
        """Custom log message format - suppress 404s for favicon and embedded files"""
        # Don't log 404s for favicon, CSS, or JS (they're embedded in HTML)
        if '404' in format and any(x in args[0] for x in ['/favicon.ico', '.css', '.js']):
            return
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def run_server(port=8000):
    """Start the HTTP server"""
    import os
    
    # Print current working directory for debugging
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # List files in current directory
    files = os.listdir('.')
    print(f"Files in directory: {', '.join(files)}")
    print()
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, PortfolioHandler)
    
    print(f"""
===============================================================
    Investment Portfolio Tracker - Backend Server
===============================================================

Server running on: http://localhost:{port}
Frontend URL:      http://localhost:{port}/

API Endpoints:
  GET /api/stock/<symbol>     - Get stock data
  GET /api/crypto/<symbol>    - Get cryptocurrency data
  GET /api/news               - Get financial news

Press Ctrl+C to stop the server
""")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.")


if __name__ == '__main__':
    # Check if API keys are set
    if ALPHA_VANTAGE_KEY == 'YOUR_ALPHA_VANTAGE_KEY':
        print("WARNING: Alpha Vantage API key not set!")
        print("Set environment variable: export ALPHA_VANTAGE_KEY='your_key_here'")
        print("Or edit the script to add your key directly")
    
    if NEWS_API_KEY == 'YOUR_NEWS_API_KEY':
        print("WARNING: News API key not set!")
        print("Set environment variable: export NEWS_API_KEY='your_key_here'")
        print("Or edit the script to add your key directly")
    
    print("\nStarting server...")
    run_server()
