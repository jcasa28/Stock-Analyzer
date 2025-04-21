import requests
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os

st.set_page_config( page_title="Stock Dashboard", page_icon="📈")

API_KEY_NEWS = st.secrets["NEWS_API_KEY"]

#initialize session state variables
if 'favorite_stocks' not in st.session_state:
    st.session_state['favorite_stocks'] = []
if 'stock_views' not in st.session_state:
    st.session_state['stock_views'] = {}
# Initialize notes session state variables
if 'notes' not in st.session_state:
    st.session_state['notes'] = {}
if 'categories' not in st.session_state:
    st.session_state['categories'] = ["General", "Stock Analysis", "Market Trends", "Investment Ideas"]
if 'current_category' not in st.session_state:
    st.session_state['current_category'] = "General"


stock_info = {
    'AAPL': {'name': 'Apple Inc.', 'logo': 'https://logo.clearbit.com/apple.com'},
    'TSLA': {'name': 'Tesla Inc.', 'logo': 'https://logo.clearbit.com/tesla.com'},
    'GOOG': {'name': 'Alphabet Inc.', 'logo': 'https://logo.clearbit.com/google.com'},
    'MSFT': {'name': 'Microsoft Corporation', 'logo': 'https://logo.clearbit.com/microsoft.com'},
    'NVDA': {'name': 'NVIDIA Corporation', 'logo': 'https://logo.clearbit.com/nvidia.com'},
    'AMZN': {'name': 'Amazon.com Inc.', 'logo': 'https://logo.clearbit.com/amazon.com'},
    'META': {'name': 'Meta Platforms, Inc.', 'logo': 'https://logo.clearbit.com/meta.com'},
    'BABA': {'name': 'Alibaba Group Holding Limited', 'logo': 'https://logo.clearbit.com/alibaba.com'},
    'DIS': {'name': 'The Walt Disney Company', 'logo': 'https://logo.clearbit.com/disney.com'},
    'NFLX': {'name': 'Netflix Inc.', 'logo': 'https://logo.clearbit.com/netflix.com'},
}


#callback functions for buttons
def toggle_favorite(stock):
    if stock in st.session_state['favorite_stocks']:
        st.session_state['favorite_stocks'].remove(stock)
    else:
        st.session_state['favorite_stocks'].append(stock)


def toggle_view(stock):
    if stock in st.session_state['stock_views'] and st.session_state['stock_views'][stock]:
        st.session_state['stock_views'][stock] = False
    else:
        # Reset all other views first
        for s in st.session_state['stock_views']:
            st.session_state['stock_views'][s] = False
        st.session_state['stock_views'][stock] = True


def display_stock_graph(stock, tab_id):
    """Display a stock's performance graph"""
    st.subheader(f'{stock} - Performance Over the Last Month')

    #fetch stock data using yfinance
    data = yf.download(tickers=stock, period='1mo', interval='1d', progress=False, auto_adjust=True)

    if data.empty:
        st.write(f"⚠️ No data returned for {stock}. Possibly invalid symbol or network issue.")
    else:
        #plotting the graph
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=1)
        ax.set_title(f'{stock} - Closing Prices Over the Last Month', fontsize=12)
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Closing Price (USD)', fontsize=10)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        plt.close()

    #use a callback for the close button
    if st.button("Close Graph", key=f"close-{stock}-{tab_id}"):
        st.session_state['stock_views'][stock] = False
        st.rerun()  # Fixed: Using st.rerun() instead of experimental_rerun


def render_stock_item(stock, tab_id):
    """Render a stock listing with buttons and info"""
    # Initialize view state for this stock if not exists
    if stock not in st.session_state['stock_views']:
        st.session_state['stock_views'][stock] = False

    in_favorites = stock in st.session_state['favorite_stocks']

    col1, col2, col3, col4 = st.columns([0.5, 0.5, 3, 1])

    with col1:
        # Use callbacks instead of direct rerun
        if in_favorites:
            if st.button("❌", key=f"remove-{stock}-{tab_id}", on_click=toggle_favorite, args=(stock,),
                         use_container_width=True):
                pass  # The action is handled by the callback
        else:
            if st.button("⭐", key=f"add-{stock}-{tab_id}", on_click=toggle_favorite, args=(stock,),
                         use_container_width=True):
                pass  # The action is handled by the callback

    with col2:
        st.image(stock_info[stock]['logo'], width=30)

    with col3:
        st.markdown(f'<div class="stock-name">{stock_info[stock]["name"]} ({stock})</div>', unsafe_allow_html=True)

    with col4:
        # Use callback for view button
        if st.button(f"📈 View", key=f"view-{stock}-{tab_id}", on_click=toggle_view, args=(stock,),
                     use_container_width=True):
            pass  # The action is handled by the callback

    # Display graph if this stock is selected for viewing
    if st.session_state['stock_views'].get(stock, False):
        display_stock_graph(stock, tab_id)


#page title
st.title('Stock Market Dashboard 📊')

#add tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["News", "Stocks", "My Favorites", "Notes 📝"])

#tab 1: News
with tab1:
    st.subheader('Latest Financial News 📰')
    st.divider()

    # Fetch recent financial news articles
    try:
        url = f"https://newsapi.org/v2/everything?q=stocks&language=en&sortBy=publishedAt&apiKey={API_KEY_NEWS}"
        response = requests.get(url)

        if response.status_code == 200:
            news_data = response.json().get("articles", [])

            if not news_data:
                st.warning("No news articles found.")

            for i, article in enumerate(news_data[:5]):  # Displaying first 5 articles
                title = article.get('title', '')
                description = article.get('description', '')
                url = article.get('url', '')
                image_url = article.get('urlToImage', '')

                if title:
                    st.subheader(title)

                if description:
                    st.write(description)

                if image_url:
                    st.image(image_url, caption="Article Image", width=300, use_container_width='auto')

                if url:
                    st.markdown(f"[Read more]({url})", unsafe_allow_html=True)

                st.divider()  # Improved visual separator between news articles
        else:
            st.error(f"Error fetching news: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching news: {e}")

#tab 2: Stocks
with tab2:
    st.subheader('Stock Market Analysis 📈')

    # Add a search box for filtering stocks
    search_query = st.text_input("Search Stock Symbol", value="", placeholder="Type a stock symbol...")
    st.divider()

    # Filter stocks based on search query
    all_stocks = list(stock_info.keys())
    if search_query:
        filtered_stocks = [stock for stock in all_stocks if search_query.upper() in stock]
    else:
        filtered_stocks = all_stocks

    # Display stocks with logos, names, and buttons
    for stock in filtered_stocks:
        with st.container():
            render_stock_item(stock, "tab2")
            st.divider()

#tab 3: My Favorites
with tab3:
    st.subheader("My Favorite Stocks 🌟")

    if st.session_state['favorite_stocks']:
        for stock in st.session_state['favorite_stocks']:
            with st.container():
                render_stock_item(stock, "tab3")
    else:
        st.write("You have not added any stocks to your favorites.")
        st.write("Go to the Stocks tab and click the ⭐ button to add stocks to your favorites.")

#tab 4: Notes
with tab4:
    st.subheader("My Investment Notes 📝")
    st.divider()
    col1, col_divider, col2 = st.columns([1, 0.02, 3])

    with col1:
        st.subheader("Categories")

        # display existing categories
        for category in st.session_state['categories']:
            if st.button(f"📁 {category}", key=f"cat-{category}", use_container_width=True):
                st.session_state['current_category'] = category
                st.rerun()

        #Add new category
        st.divider()
        new_category = st.text_input("Add new category:", key="new_category", placeholder="Enter category name")
        if st.button("➕ Add Category", use_container_width=True):
            if new_category and new_category not in st.session_state['categories']:
                st.session_state['categories'].append(new_category)
                # Initialize empty notes list for the new category
                if new_category not in st.session_state['notes']:
                    st.session_state['notes'][new_category] = []
                st.success(f"Added category: {new_category}")
                st.rerun()
            elif new_category in st.session_state['categories']:
                st.error("Category already exists!")
            else:
                st.error("Please enter a category name.")

    with col_divider:
        st.markdown(
            "<div style='border-left: 1px solid #bbb; height: 100%;'></div>",
            unsafe_allow_html=True
        )

    with col2:
        current_cat = st.session_state['current_category']
        st.subheader(f"Notes for: {current_cat}")

        # Initialize notes for current category if not exists
        if current_cat not in st.session_state['notes']:
            st.session_state['notes'][current_cat] = []

        # add new note
        with st.expander("Add New Note", expanded=False):
            note_title = st.text_input("Title:", key=f"title-{current_cat}", placeholder="Enter note title")
            note_content = st.text_area("Content:", key=f"content-{current_cat}",
                                        placeholder="Write your notes here...", height=150)

            related_stocks = st.multiselect("Related Stocks:", options=all_stocks,
                                            key=f"stocks-{current_cat}")

            date_added = datetime.now().strftime("%Y-%m-%d %H:%M")

            if st.button("💾 Save Note", use_container_width=True):
                if note_title and note_content:
                    new_note = {
                        "title": note_title,
                        "content": note_content,
                        "date": date_added,
                        "related_stocks": related_stocks
                    }
                    st.session_state['notes'][current_cat].append(new_note)
                    st.success("Note saved successfully!")
                    st.rerun()
                else:
                    st.error("Please provide both title and content.")

        # Display existing notes
        if not st.session_state['notes'].get(current_cat, []):
            st.info(f"No notes in the '{current_cat}' category. Add your first note above.")
        else:
            for i, note in enumerate(st.session_state['notes'][current_cat]):
                with st.expander(f"📌 {note['title']} - {note['date']}"):
                    st.markdown(f"**Date:** {note['date']}")

                    # Display related stocks as chips/badges
                    if note['related_stocks']:
                        stock_badges = " ".join([f"<span style='background-color: #f0f2f6; padding: 2px 8px; "
                                                 f"border-radius: 10px; margin-right: 5px;'>{s}</span>"
                                                 for s in note['related_stocks']])
                        st.markdown(f"**Related Stocks:** {stock_badges}", unsafe_allow_html=True)

                    st.divider()
                    st.markdown(note['content'])

                    # Edit and delete buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit-{current_cat}-{i}", use_container_width=True):
                            # Set up edit session state
                            st.session_state[f'edit_title_{current_cat}_{i}'] = note['title']
                            st.session_state[f'edit_content_{current_cat}_{i}'] = note['content']
                            st.session_state[f'edit_stocks_{current_cat}_{i}'] = note['related_stocks']
                            st.session_state[f'editing_{current_cat}_{i}'] = True
                            st.rerun()

                    with col2:
                        if st.button("🗑️ Delete", key=f"delete-{current_cat}-{i}", use_container_width=True):
                            st.session_state['notes'][current_cat].pop(i)
                            st.success("Note deleted!")
                            st.rerun()

                # Check if we're editing this note
                if st.session_state.get(f'editing_{current_cat}_{i}', False):
                    with st.expander("Edit Note", expanded=True):
                        edited_title = st.text_input("Title:",
                                                     value=st.session_state[f'edit_title_{current_cat}_{i}'],
                                                     key=f"edit_title_input_{i}")

                        edited_content = st.text_area("Content:",
                                                      value=st.session_state[f'edit_content_{current_cat}_{i}'],
                                                      key=f"edit_content_input_{i}",
                                                      height=150)

                        edited_stocks = st.multiselect("Related Stocks:",
                                                       options=all_stocks,
                                                       default=st.session_state[f'edit_stocks_{current_cat}_{i}'],
                                                       key=f"edit_stocks_input_{i}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("💾 Save Changes", key=f"save_edit_{i}", use_container_width=True):
                                # Update note
                                st.session_state['notes'][current_cat][i]["title"] = edited_title
                                st.session_state['notes'][current_cat][i]["content"] = edited_content
                                st.session_state['notes'][current_cat][i]["related_stocks"] = edited_stocks
                                st.session_state['notes'][current_cat][i]["date"] = f"{note['date']} (edited)"

                                # Clear edit state
                                st.session_state[f'editing_{current_cat}_{i}'] = False
                                st.success("Note updated successfully!")
                                st.rerun()

                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_edit_{i}", use_container_width=True):
                                #  Clear edit state
                                st.session_state[f'editing_{current_cat}_{i}'] = False
                                st.rerun()