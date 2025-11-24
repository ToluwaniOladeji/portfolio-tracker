# Investment Portfolio Tracker

A real-time investment portfolio tracking application that helps users monitor their stocks and cryptocurrency investments with live market data and financial news. Built with pure Python (no frameworks) on the backend and vanilla JavaScript on the frontend.

![Portfolio Tracker](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)

## 🌟 Features

- **Real-time Stock Tracking**: Monitor stock prices using Alpha Vantage API
- **Cryptocurrency Support**: Track crypto assets via CoinGecko API  
- **Financial News Feed**: Stay updated with latest business news from News API
- **Portfolio Management**: Add, remove, and track multiple assets with purchase history
- **Interactive Data Controls**:
  - Sort by symbol, value, or gain/loss percentage
  - Filter by asset type (stocks/crypto)
  - Real-time search functionality across portfolio
- **Performance Metrics**: View total portfolio value, profit/loss, and asset count
- **Smart Dropdowns**: 30 popular stocks and 15 cryptocurrencies pre-loaded
- **Data Persistence**: Portfolio saved in browser localStorage
- **Responsive Design**: Modern UI that works on desktop and mobile
- **Load Balanced Deployment**: Configured for high availability with HAProxy
- **Error Handling**: Comprehensive error management for API failures

## 🔧 Technologies Used

### Backend
- **Python 3.8+** - Pure Python HTTP server (no frameworks)
- **Standard Library Only** - No external dependencies required
- Built-in modules: `http.server`, `urllib`, `json`, `ssl`

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern responsive design with custom styling
- **Vanilla JavaScript** - No frameworks or libraries
- **LocalStorage API** - Client-side data persistence

### APIs
- **[Alpha Vantage API](https://www.alphavantage.co/)** - Stock market data
- **[CoinGecko API](https://www.coingecko.com/en/api)** - Cryptocurrency prices
- **[News API](https://newsapi.org/)** - Financial news headlines

### Infrastructure
- **HAProxy** - Load balancing between multiple servers
- **Ubuntu Linux** - Web server hosting
- **SSH/SCP** - Secure file transfer and remote access

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection for API calls
- Web browser (Chrome, Firefox, Safari, or Edge)
- For deployment: 2 web servers + 1 load balancer with HAProxy

## 🚀 Local Setup & Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/portfolio-tracker.git
cd portfolio-tracker
```

### Step 2: Get API Keys

#### Alpha Vantage (Stock Data)
1. Visit: https://www.alphavantage.co/support/#api-key
2. Click "Get Free API Key"
3. Fill out form and receive key instantly
4. Free tier: 25 requests/day, 5 requests/minute

#### News API (Financial News)  
1. Visit: https://newsapi.org/register
2. Register for free account
3. Get API key from dashboard
4. Free tier: 100 requests/day (development only)

#### CoinGecko (Cryptocurrency)
- **No API key required!** 
- Free tier: 50 calls/minute
- No registration needed

### Step 3: Configure API Keys

**Option A: Environment Variables (Recommended)**
```bash
# Linux/Mac
export ALPHA_VANTAGE_KEY='your_alpha_vantage_key_here'
export NEWS_API_KEY='your_news_api_key_here'

# Windows Command Prompt
set ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here
set NEWS_API_KEY=your_news_api_key_here

# Windows PowerShell
$env:ALPHA_VANTAGE_KEY='your_alpha_vantage_key_here'
$env:NEWS_API_KEY='your_news_api_key_here'
```

**Option B: Edit server.py Directly**
Open `server.py` and modify lines 16-17:
```python
ALPHA_VANTAGE_KEY = 'your_actual_alpha_key_here'
NEWS_API_KEY = 'your_actual_news_key_here'
```

⚠️ **WARNING**: If editing server.py, DO NOT commit to GitHub!

### Step 4: Run the Application

```bash
python3 server.py
```

You should see:
```
===============================================================
    Investment Portfolio Tracker - Backend Server
===============================================================

Server running on: http://localhost:8000
```

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## 🎯 Usage Guide

### Adding Assets

1. **Select Asset Type**: Choose "Stock" or "Cryptocurrency" from dropdown
2. **Choose Symbol**: Select from popular assets or type custom symbol
   - **Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, etc.
   - **Crypto**: BTC, ETH, BNB, SOL, XRP, etc.
3. **Enter Quantity**: How many shares/coins you own
4. **Purchase Price** (Optional): Defaults to current price if left empty
5. Click **"Add to Portfolio"**

### Managing Your Portfolio

- **Sort**: Click dropdown to organize by symbol, value, or gain/loss
- **Filter**: Show all assets, stocks only, or crypto only
- **Search**: Type to find specific assets in your portfolio
- **Delete**: Remove assets by clicking the delete button
- **View Details**: See purchase price, current price, and profit/loss

### Understanding Metrics

- **Total Value**: Current worth of all holdings
- **Profit/Loss**: Total gain or loss since purchase
- **Total Assets**: Number of different assets in portfolio
- **Gain/Loss %**: Percentage change for each asset

## 🌐 Deployment to Web Servers

### Architecture Overview

```
Internet → Load Balancer (HAProxy) → Web Server 01 (Python)
                                   → Web Server 02 (Python)
```

### Prerequisites
- 2 Ubuntu web servers (Web01, Web02)
- 1 Ubuntu load balancer with HAProxy installed
- SSH access to all servers

### Step-by-Step Deployment

#### 1. Deploy to Web01

**Connect via SSH:**
```bash
ssh ubuntu@<WEB01_IP>
```

**Create directory:**
```bash
mkdir -p ~/portfolio-tracker
cd ~/portfolio-tracker
```

**Upload files from local machine (new terminal):**
```bash
scp index.html ubuntu@<WEB01_IP>:~/portfolio-tracker/
scp style.css ubuntu@<WEB01_IP>:~/portfolio-tracker/
scp app.js ubuntu@<WEB01_IP>:~/portfolio-tracker/
scp server.py ubuntu@<WEB01_IP>:~/portfolio-tracker/
```

**Set API keys and start server:**
```bash
export ALPHA_VANTAGE_KEY='your_key'
export NEWS_API_KEY='your_key'
cd ~/portfolio-tracker
nohup python3 server.py > server.log 2>&1 &
```

**Verify server is running:**
```bash
ps aux | grep server.py
netstat -tulpn | grep :8000
curl http://localhost:8000/api/news
```

**Configure firewall:**
```bash
sudo ufw allow 8000
sudo ufw status
```

#### 2. Deploy to Web02

Repeat all steps from Web01, replacing `<WEB01_IP>` with `<WEB02_IP>`.

#### 3. Configure Load Balancer

**Connect to load balancer:**
```bash
ssh ubuntu@<LB01_IP>
```

**Edit HAProxy configuration:**
```bash
sudo nano /etc/haproxy/haproxy.cfg
```

**Add/Update configuration:**
```
global
    log /dev/log local0
    log /dev/log local1 notice
    maxconn 2000
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend web-backend

backend web-backend
    balance roundrobin
    option httpchk GET /api/news
    http-check expect status 200
    server web01 <WEB01_IP>:8000 check
    server web02 <WEB02_IP>:8000 check

listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
```

**Test and restart:**
```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
sudo systemctl restart haproxy
sudo systemctl status haproxy
```

#### 4. Verify Deployment

**Test individual servers:**
```bash
curl http://<WEB01_IP>:8000/api/news
curl http://<WEB02_IP>:8000/api/news
```

**Test load balancer:**
```bash
curl http://<LB01_IP>/api/news
```

**Access in browser:**
```
http://<LB01_IP>
```

**View HAProxy statistics:**
```
http://<LB01_IP>:8404/stats
```

Both servers should show **UP** status in green.

## 📁 Project Structure

```
portfolio-tracker/
├── index.html              # Main HTML structure
├── style.css               # Custom CSS styling
├── app.js                  # Frontend JavaScript logic
├── server.py               # Python backend server
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
```

## 🔐 Security Best Practices

- ✅ **Never commit API keys** to version control
- ✅ **Use environment variables** for sensitive data
- ✅ **Add .gitignore** to exclude secrets
- ✅ **Respect API rate limits** to avoid blocks
- ✅ **Validate all user inputs** on backend
- ✅ **Use HTTPS** in production environments
- ✅ **Regular security updates** for dependencies

## 🐛 Troubleshooting

### Server Won't Start

**Error**: "Address already in use"
```bash
# Kill existing process
pkill -f server.py
# Or find and kill specific PID
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Error**: "Python not found"
```bash
# Check Python version
python3 --version
# Install if needed (Ubuntu)
sudo apt update
sudo apt install python3
```

### API Issues

**Problem**: "API key invalid"
- Verify keys are correct (no extra spaces)
- Check if keys are properly set: `echo $ALPHA_VANTAGE_KEY`
- Regenerate keys if necessary

**Problem**: "Rate limit exceeded"
- Alpha Vantage: Wait until next day (25 requests/day)
- News API: Wait until next day (100 requests/day)
- CoinGecko: Wait 1 minute (50 calls/minute)

### Deployment Issues

**Problem**: "503 Service Unavailable"
- Check if servers are running: `ps aux | grep server.py`
- Verify ports are open: `netstat -tulpn | grep :8000`
- Check HAProxy logs: `sudo tail -f /var/log/haproxy.log`

**Problem**: "Connection refused"
- Verify firewall allows port 8000: `sudo ufw allow 8000`
- Check server is binding to all interfaces (0.0.0.0)
- Ensure HAProxy has correct server IPs

### Browser Issues

**Problem**: "No news available"
- Open browser console (F12)
- Check for CORS errors
- Verify News API key is set correctly
- Test API directly: `curl http://localhost:8000/api/news`

**Problem**: "Assets not persisting"
- Check if localStorage is enabled in browser
- Clear browser cache and reload
- Check browser console for errors

## 📊 API Documentation & Credits

### Alpha Vantage
- **Purpose**: Real-time and historical stock market data
- **Documentation**: https://www.alphavantage.co/documentation/
- **Free Tier**: 25 requests/day, 5 requests/minute
- **Used For**: Stock prices, company information, market data

### CoinGecko  
- **Purpose**: Cryptocurrency market data and prices
- **Documentation**: https://www.coingecko.com/en/api/documentation
- **Free Tier**: 50 calls/minute (no API key required)
- **Used For**: Crypto prices, 24h changes, market volumes

### News API
- **Purpose**: Financial and business news headlines
- **Documentation**: https://newsapi.org/docs
- **Free Tier**: 100 requests/day (development only)
- **Used For**: Latest business news, market updates

## 🎓 Challenges & Solutions

### Challenge 1: API Rate Limiting
**Problem**: Alpha Vantage's free tier only allows 25 requests per day, which is quickly exhausted during testing.

**Solution**: Implemented client-side caching using localStorage to store portfolio data. This reduces API calls significantly as we only fetch current prices when adding new assets, not on every page load. Additionally, added clear error messages when rate limits are reached.

### Challenge 2: No Framework Requirement
**Problem**: Building an HTTP server without using frameworks like Flask or Django meant implementing routing, CORS, and file serving manually.

**Solution**: Used Python's built-in `http.server.BaseHTTPRequestHandler` to create custom request handlers. Implemented manual routing by parsing URL paths and serving different content types (HTML, CSS, JS, JSON) based on file extensions. Added custom CORS headers to all responses.

### Challenge 3: Windows Compatibility
**Problem**: The server initially used Unicode box-drawing characters that caused encoding errors on Windows machines.

**Solution**: Replaced special characters with ASCII-safe alternatives in server output. This ensured the application runs smoothly on Windows, Linux, and macOS without encoding issues.

### Challenge 4: Load Balancer Health Checks
**Problem**: HAProxy needed a reliable endpoint to check if backend servers were healthy, but simple HTTP GET on root path wasn't sufficient.

**Solution**: Configured HAProxy to use `/api/news` as the health check endpoint since it tests both the server and API connectivity. Added proper HTTP status code checking to ensure servers are truly functional before routing traffic.

### Challenge 5: Persistent Environment Variables
**Problem**: Environment variables set in SSH sessions don't persist after disconnection, causing servers to fail on restart.

**Solution**: Provided two approaches: (1) Hardcode API keys directly in server.py for simplicity (with warning not to commit), and (2) Add exports to `~/.bashrc` for persistence across sessions. Documented both methods clearly.

### Challenge 6: Asset Symbol Management
**Problem**: Users had to manually type stock/crypto symbols, leading to errors with invalid symbols.

**Solution**: Created comprehensive dropdown lists with 30 popular stocks and 15 cryptocurrencies. Implemented cascading dropdowns where selecting the asset type populates appropriate symbols, reducing user error and improving UX.

## 🎬 Demo Video

**Hosted**: [YouTube/Vimeo/Google Drive Link]


## 🙏 Acknowledgments

- **Alpha Vantage** - For providing free stock market data API
- **CoinGecko** - For cryptocurrency market data without requiring API keys
- **News API** - For financial news headlines and business updates
- **Python Software Foundation** - For Python and standard library
- **HAProxy Technologies** - For open-source load balancing software
- **Inter Font** - For modern typography (Google Fonts)

## 📄 License

This project is created for educational purposes as part of a university assignment.

## 👤 Author

Oladeji Toluwani Jephthae
- Email: t.oladeji@alustudent.com
- GitHub: https://github.com/ToluwaniOladeji

## 📅 Project Information

- **Course**: Web Infrastructure
- **Assignment**: Playing Around with APIs
- **Submission Date**: November 24, 2025
- **Institution**: African Leadership University

---

November 24, 2025

---

**Note**: This application is designed for educational purposes. For production use, consider implementing additional security measures, caching strategies, and error handling.
