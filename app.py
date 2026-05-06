from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import re
import os

app = Flask(__name__)
CORS(app)

# 1. Load your data
df = pd.read_csv('products.csv')

# 2. ADD YOUR EXISTING BOT LOGIC HERE (from product_insight_bot.py)
def analyze_query(question):
    question = question.lower().strip()

    if question == 'help':
        return show_help()
    if question in ['quit', 'exit', 'bye']:
        return "Thank you for using ProductInsightBot!"

    # Enhanced keyword detection with context
    if 'most expensive' in question:
        return find_most_expensive(question)
    if 'cheapest' in question or 'least expensive' in question:
        return find_cheapest(question)
    if 'rating above' in question or 'rating over' in question:
        return filter_by_rating(question)
    if any(x in question for x in ['under', 'below', 'less than']):
        return filter_by_max_price(question)
    if 'average price' in question:
        return calculate_average_price(question)
    if 'most reviews' in question:
        return find_most_reviews(question)
    if 'price range' in question:
        return show_price_range(question)
    if any(word in question for word in ['categories', 'types']):
        return show_categories()

    if any(cat in question for cat in ['smartwatch', 'luxury', 'sports', 'fashion', 'digital', 'analog']):
        return category_analysis(question)
    if any(brand in question for brand in ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']):
        return brand_analysis(question)

    return "I'm not sure I understand. Try asking about smartwatches, luxury watches, prices, or ratings or type 'help' for examples."

# ADD ALL YOUR EXISTING FUNCTIONS HERE:
def find_most_expensive(question):
    filtered_df = df
    categories = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital', 'analog': 'Analog'
    }
    brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
    
    for key, category in categories.items():
        if key in question:
            filtered_df = filtered_df[filtered_df['category'] == category]
            break
    
    for brand in brands:
        if brand in question:
            filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
            break
    
    if filtered_df.empty:
        return "❌ No products found matching your criteria."
    
    max_price_idx = filtered_df['price'].idxmax()
    product = filtered_df.loc[max_price_idx]
    return f"💰 Most Expensive: {product['product_name']} - ₹{product['price']:,} (Rating: {product['rating']}⭐)"

def find_cheapest(question):
    filtered_df = df
    categories = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital', 'analog': 'Analog'
    }
    brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
    
    for key, category in categories.items():
        if key in question:
            filtered_df = filtered_df[filtered_df['category'] == category]
            break
    
    for brand in brands:
        if brand in question:
            filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
            break
    
    if filtered_df.empty:
        return "❌ No products found matching your criteria."
    
    min_price_idx = filtered_df['price'].idxmin()
    product = filtered_df.loc[min_price_idx]
    return f"💸 Cheapest: {product['product_name']} - ₹{product['price']:,} (Rating: {product['rating']}⭐)"

def filter_by_max_price(question):
    numbers = re.findall(r'[\d.]+', question)
    if not numbers:
        return "Please specify a price (e.g., 'watches under 10000')"

    max_price = float(numbers[0])
    affordable_items = df[df['price'] <= max_price]

    if affordable_items.empty:
        return f"No watches found under ₹{max_price:,}"

    results = "\n".join([
        f"{row['product_name']} - ₹{row['price']:,} (Rating: {row['rating']})"
        for _, row in affordable_items.head(8).iterrows()
    ])
    return f"🛍️ Watches under ₹{max_price:,}:\n{results}"

def filter_by_rating(question):
    numbers = re.findall(r'[\d.]+', question)
    if not numbers:
        return "Please specify a rating threshold (e.g., 'rating above 4.5')"

    threshold = float(numbers[0])
    high_rated = df[df['rating'] > threshold]

    if high_rated.empty:
        return f"No watches found with rating above {threshold}"

    results = "\n".join([
        f"⭐ {row['product_name']} - ₹{row['price']:,} (Rating: {row['rating']})"
        for _, row in high_rated.head(8).iterrows()
    ])
    return f"Watches with rating above {threshold}:\n{results}"

def find_most_reviews(question):
    filtered_df = df
    categories = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital', 'analog': 'Analog'
    }
    brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
    
    for key, category in categories.items():
        if key in question:
            filtered_df = filtered_df[filtered_df['category'] == category]
            break
    
    for brand in brands:
        if brand in question:
            filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
            break
    
    if filtered_df.empty:
        return "❌ No products found matching your criteria."
    
    max_reviews_idx = filtered_df['reviews'].idxmax()
    product = filtered_df.loc[max_reviews_idx]
    return f"📝 Most Reviews: {product['product_name']} - {product['reviews']:,} reviews (Rating: {product['rating']}⭐)"

def calculate_average_price(question):
    category_map = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital'
    }

    for key, category in category_map.items():
        if key in question:
            avg_price = df[df['category'] == category]['price'].mean()
            return f"📊 Average price of {category.lower()} watches: ₹{avg_price:,.2f}"

    overall_avg = df['price'].mean()
    return f"📊 Average price of all watches: ₹{overall_avg:,.2f}"

def category_analysis(question):
    categories = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital', 'analog': 'Analog'
    }

    results = []
    for key, name in categories.items():
        if key in question:
            subset = df[df['category'] == name]
            if not subset.empty:
                avg_price = subset['price'].mean()
                avg_rating = subset['rating'].mean()
                results.append(f"{name}: {len(subset)} watches, Avg ₹{avg_price:,.2f}, Rating {avg_rating:.1f}⭐")

    return "\n".join(results) if results else "I can analyze: smartwatch, luxury, sports, fashion, digital, or analog watches."

def brand_analysis(question):
    brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
    results = []

    for brand in brands:
        if brand in question:
            subset = df[df['brand'].str.lower().str.contains(brand)]
            if not subset.empty:
                avg_price = subset['price'].mean()
                avg_rating = subset['rating'].mean()
                results.append(f"{brand.title()}: {len(subset)} watches, Avg ₹{avg_price:,.2f}, Rating {avg_rating:.1f}⭐")

    return "\n".join(results) if results else "Try: Titan, Casio, Fastrack, Sonata, Fossil, Samsung, Apple, or Noise."

def show_price_range(question):
    filtered_df = df
    categories = {
        'smartwatch': 'Smartwatch', 'luxury': 'Luxury', 'sports': 'Sports',
        'fashion': 'Fashion', 'digital': 'Digital', 'analog': 'Analog'
    }
    brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
    
    for key, category in categories.items():
        if key in question:
            filtered_df = filtered_df[filtered_df['category'] == category]
            break
    
    for brand in brands:
        if brand in question:
            filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
            break
    
    if filtered_df.empty:
        return "❌ No products found matching your criteria."
    
    min_price = filtered_df['price'].min()
    max_price = filtered_df['price'].max()
    return f"📈 Price Range: ₹{min_price:,} - ₹{max_price:,}"

def show_categories():
    category_counts = df['category'].value_counts()
    result = ["Watch Categories:"]
    for category, count in category_counts.items():
        avg_price = df[df['category'] == category]['price'].mean()
        result.append(f"• {category}: {count} watches (Avg ₹{avg_price:,.2f})")
    return "\n".join(result)

def show_help():
    return """
ProductInsightBot: Watch Support Overview

SMARTWATCHES:
-> "Most expensive smartwatch"
-> "Smartwatches under 15000"
-> "Apple smartwatch analysis"

LUXURY WATCHES:
-> "Average price of luxury watches"
-> "Luxury watches under 50000"
-> "Fossil luxury watches"

SPORTS WATCHES:
-> "Cheapest sports watch"
-> "Casio sports watches analysis"
-> "Sports watches with high ratings"

FASHION WATCHES:
-> "Fashion watches price range"

DIGITAL WATCHES:
-> "Digital watches reviews"

ANALOG WATCHES:
-> "Analog watches under 8000"

PRICE QUERIES:
-> "Most expensive watch"
-> "Watches under 10000"
-> "Price range overall"

RATING QUERIES:
-> "Highest rated watches"
-> "Watches with rating above 4.5"

BRAND QUERIES:
-> "Compare Titan and Casio"
-> "Fastrack vs Sonata prices"
-> "Samsung watch analysis"

GENERAL:
-> "Show categories"
-> "Watch with most reviews"
-> "Compare smartwatches and luxury watches"
"""

# 3. API route (keep this as is)
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    response = analyze_query(question)  # Uses your REAL Python logic!
    return jsonify({'response': response})

# 4. Serve your frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)