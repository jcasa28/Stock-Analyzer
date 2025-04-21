# Stock Market Dashboard 📊

This interactive Streamlit application allows users to effectively monitor stock market performance, track favorite stocks, view financial news, and manage investment notes in a clear and user-friendly interface.

## Author

**Jesus Casasanta**
PID: 6450917

## Features

- **Latest Financial News:** Fetches real-time financial news, displaying titles, summaries, images, and external links.
- **Stock Analysis:** Provides interactive visualizations showing recent stock performance using Yahoo Finance historical data.
- **Favorites Management:** Easily manage and track favorite stocks by adding or removing them.
- **Investment Notes:** Add, edit, categorize, and link notes to specific stocks for detailed investment tracking.

## Technologies Used

- **Streamlit:** Web-based user interface for interactive dashboards.
- **Requests:** For API interactions, primarily fetching financial news from the News API.
- **yfinance:** Provides reliable stock data retrieval.
- **Matplotlib:** Visualizes stock price trends graphically.
- **Pandas:** Manipulates and analyzes stock and financial news data.



## API Integration

- **News API ([newsapi.org](https://newsapi.org/)):** Retrieves recent financial news.
- **Yahoo Finance (yfinance):** Provides stock market data for analysis and graphing.

## Installation & Setup


### Step 1: Install Dependencies
```bash
pip install pandas streamlit requests yfinance matplotlib
```

### Step 2: Configure API Key
Create a `.env` file or use Streamlit Secrets and insert your News API key:
```bash
NEWS_API_KEY=your_newsapi_key_here
```

### Step 4: Launch the Application
```bash
streamlit run stock_display.py
```

## Usability Goals

- **Effectiveness:** Ensures reliable and up-to-date financial information.
- **Efficiency:** Quick interactions with a responsive UI, streamlined navigation.
- **Learnability:** Intuitive design ideal for both beginners and experienced investors.
- **User Satisfaction:** Visually appealing, easy-to-use interface.

## Future Improvements

- Integration of additional interactive widgets (dropdowns, sliders).
- Expand available data sources and analytics capabilities.
- Enhance user interface styling and add custom theming.


