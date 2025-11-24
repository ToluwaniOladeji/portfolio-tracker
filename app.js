/ Configuration
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? `http://${window.location.hostname}:${window.location.port || 8000}` 
    : '';

let portfolio = [];
let allNews = [];

// Popular stocks and cryptocurrencies
const STOCKS = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'MSFT', name: 'Microsoft Corporation' },
    { symbol: 'GOOGL', name: 'Alphabet Inc. (Google)' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.' },
    { symbol: 'TSLA', name: 'Tesla Inc.' },
    { symbol: 'META', name: 'Meta Platforms (Facebook)' },
    { symbol: 'NVDA', name: 'NVIDIA Corporation' },
    { symbol: 'JPM', name: 'JPMorgan Chase & Co.' },
    { symbol: 'V', name: 'Visa Inc.' },
    { symbol: 'JNJ', name: 'Johnson & Johnson' },
    { symbol: 'WMT', name: 'Walmart Inc.' },
    { symbol: 'PG', name: 'Procter & Gamble' },
    { symbol: 'MA', name: 'Mastercard Inc.' },
    { symbol: 'HD', name: 'The Home Depot' },
    { symbol: 'DIS', name: 'The Walt Disney Company' },
    { symbol: 'NFLX', name: 'Netflix Inc.' },
    { symbol: 'PYPL', name: 'PayPal Holdings' },
    { symbol: 'ADBE', name: 'Adobe Inc.' },
    { symbol: 'INTC', name: 'Intel Corporation' },
    { symbol: 'CMCSA', name: 'Comcast Corporation' },
    { symbol: 'KO', name: 'The Coca-Cola Company' },
    { symbol: 'PEP', name: 'PepsiCo Inc.' },
    { symbol: 'CSCO', name: 'Cisco Systems' },
    { symbol: 'XOM', name: 'Exxon Mobil Corporation' },
    { symbol: 'CVX', name: 'Chevron Corporation' },
    { symbol: 'BA', name: 'The Boeing Company' },
    { symbol: 'IBM', name: 'IBM' },
    { symbol: 'ORCL', name: 'Oracle Corporation' },
    { symbol: 'AMD', name: 'Advanced Micro Devices' },
    { symbol: 'NKE', name: 'Nike Inc.' }
];

const CRYPTOCURRENCIES = [
    { symbol: 'BTC', name: 'Bitcoin' },
    { symbol: 'ETH', name: 'Ethereum' },
    { symbol: 'USDT', name: 'Tether' },
    { symbol: 'BNB', name: 'Binance Coin' },
    { symbol: 'SOL', name: 'Solana' },
    { symbol: 'XRP', name: 'Ripple' },
    { symbol: 'ADA', name: 'Cardano' },
    { symbol: 'DOGE', name: 'Dogecoin' },
    { symbol: 'DOT', name: 'Polkadot' },
    { symbol: 'MATIC', name: 'Polygon' },
    { symbol: 'LTC', name: 'Litecoin' },
    { symbol: 'LINK', name: 'Chainlink' },
    { symbol: 'UNI', name: 'Uniswap' },
    { symbol: 'AVAX', name: 'Avalanche' },
    { symbol: 'ATOM', name: 'Cosmos' }
];

// Log startup
console.log('Portfolio Tracker initialized');
console.log('API Base:', API_BASE);

// API call helper function
async function apiCall(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// Show message to user
function showMessage(message, type) {
    const container = document.getElementById('message-container');
    const div = document.createElement('div');
    div.className = type === 'error' ? 'error-message' : 'success-message';
    div.textContent = message;
    container.appendChild(div);
    setTimeout(() => div.remove(), 5000);
}

// Populate symbol dropdown based on asset type
function populateSymbolDropdown(type) {
    const symbolSelect = document.getElementById('symbol');
    symbolSelect.innerHTML = '<option value="">Select Symbol</option>';
    
    const assets = type === 'stock' ? STOCKS : CRYPTOCURRENCIES;
    
    assets.forEach(asset => {
        const option = document.createElement('option');
        option.value = asset.symbol;
        option.textContent = `${asset.symbol} - ${asset.name}`;
        symbolSelect.appendChild(option);
    });
    
    symbolSelect.disabled = false;
}

// Add asset to portfolio
async function addAsset(e) {
    e.preventDefault();
    const symbol = document.getElementById('symbol').value.toUpperCase();
    const quantity = parseFloat(document.getElementById('quantity').value);
    const purchasePrice = parseFloat(document.getElementById('purchase-price').value) || null;
    const type = document.getElementById('asset-type').value;

    if (!type) {
        showMessage('Please select an asset type', 'error');
        return;
    }

    if (!symbol) {
        showMessage('Please select a symbol', 'error');
        return;
    }

    try {
        const endpoint = type === 'stock' ? `/api/stock/${symbol}` : `/api/crypto/${symbol}`;
        const data = await apiCall(endpoint);

        if (data.error) {
            showMessage(data.error, 'error');
            return;
        }

        const currentPrice = type === 'stock' ? data.price : data.current_price;
        
        portfolio.push({
            symbol: symbol,
            name: data.name || symbol,
            type: type,
            quantity: quantity,
            currentPrice: currentPrice,
            purchasePrice: purchasePrice || currentPrice,
            currentValue: currentPrice * quantity
        });

        savePortfolio();
        renderPortfolio();
        showMessage(`${symbol} added successfully!`, 'success');
        document.getElementById('add-asset-form').reset();
        document.getElementById('symbol').disabled = true;
        document.getElementById('symbol').innerHTML = '<option value="">Select asset type first</option>';
    } catch (error) {
        showMessage(`Failed to add ${symbol}. Please check the symbol and try again.`, 'error');
    }
}

// Delete asset from portfolio
function deleteAsset(index) {
    const asset = portfolio[index];
    if (confirm(`Are you sure you want to remove ${asset.symbol}?`)) {
        portfolio.splice(index, 1);
        savePortfolio();
        renderPortfolio();
        showMessage(`${asset.symbol} removed from portfolio`, 'success');
    }
}

// Render portfolio table
function renderPortfolio() {
    const container = document.getElementById('portfolio-container');
    
    if (portfolio.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <h3>Your Portfolio is Empty</h3>
                <p>Start building your investment portfolio by adding your first asset above!</p>
            </div>
        `;
        updateSummary();
        return;
    }

    let html = `
        <table class="portfolio-table">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Quantity</th>
                    <th>Purchase Price</th>
                    <th>Current Price</th>
                    <th>Current Value</th>
                    <th>Gain/Loss</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
    `;

    portfolio.forEach((asset, index) => {
        const gainLoss = (asset.currentPrice - asset.purchasePrice) * asset.quantity;
        const gainLossPercent = ((asset.currentPrice - asset.purchasePrice) / asset.purchasePrice * 100).toFixed(2);
        const gainLossClass = gainLoss >= 0 ? 'positive' : 'negative';

        html += `
            <tr>
                <td><strong>${asset.symbol}</strong></td>
                <td>${asset.name}</td>
                <td>${asset.type === 'stock' ? '📊 Stock' : '₿ Crypto'}</td>
                <td>${asset.quantity}</td>
                <td>$${asset.purchasePrice.toFixed(2)}</td>
                <td>$${asset.currentPrice.toFixed(2)}</td>
                <td>$${asset.currentValue.toFixed(2)}</td>
                <td class="${gainLossClass}">
                    ${gainLoss >= 0 ? '+' : ''}$${gainLoss.toFixed(2)}
                    (${gainLoss >= 0 ? '+' : ''}${gainLossPercent}%)
                </td>
                <td><button class="delete-btn" onclick="deleteAsset(${index})">Delete</button></td>
            </tr>
        `;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
    updateSummary();
}
