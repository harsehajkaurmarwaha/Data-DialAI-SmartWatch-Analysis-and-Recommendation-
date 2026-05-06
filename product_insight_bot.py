import pandas as pd
import re

class ProductInsightBot:

    def __init__(self, data_source='products.csv'):
        # Initialize bot with product data
        self.data_source = data_source
        self.df = pd.read_csv(data_source)
        self.display_welcome_message()

    def display_welcome_message(self):
        # bot introduction message
        print("=" * 60)
        print("🤖 Hello and welcome! I'm ProductInsightBot, here to help you explore watch insights.")
        print("=" * 60)
        print("❔Here are a few ways I can help you with watch analysis:")
        print("   -> 'Which watch is the most expensive?'")
        print("   -> 'Show me smartwatches with rating above 4.5'")
        print("   -> 'What is the average price of luxury watches?'")
        print("   -> 'Which brand has the most reviews?'")
        print("   -> 'List watches under ₹10000'")
        print("   -> 'Compare Titan and Casio prices'")
        print("\nType 'help' for more options or 'quit' to exit.")
        print("=" * 60)

    # main query 
    def analyze_query(self, question):
        question = question.lower().strip()

        if question == 'help':
            return self.show_help()
        if question in ['quit', 'exit', 'bye']:
            return "Thank you for using ProductInsightBot!"

        # Enhanced keyword detection with context
        if 'most expensive' in question:
            return self.find_most_expensive(question)
        if 'cheapest' in question or 'least expensive' in question:
            return self.find_cheapest(question)
        if 'rating above' in question or 'rating over' in question:
            return self.filter_by_rating(question)
        if any(x in question for x in ['under', 'below', 'less than']):
            return self.filter_by_max_price(question)
        if 'average price' in question:
            return self.calculate_average_price(question)
        if 'most reviews' in question:
            return self.find_most_reviews(question)
        if 'price range' in question:
            return self.show_price_range(question)
        if any(word in question for word in ['categories', 'types']):
            return self.show_categories()

        if any(cat in question for cat in ['smartwatch', 'luxury', 'sports', 'fashion', 'digital', 'analog']):
            return self.category_analysis(question)
        if any(brand in question for brand in ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']):
            return self.brand_analysis(question)

        return "I'm not sure I understand. Try asking about smartwatches, luxury watches, prices, or ratings or type 'help' for examples."

    # FIXED: Enhanced price analysis with filtering
    def find_most_expensive(self, question):
        # Start with all data
        filtered_df = self.df
        
        # Check for category in question
        categories = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury', 
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital',
            'analog': 'Analog'
        }
        
        # Check for brand in question
        brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
        
        # Apply category filter if mentioned
        category_used = None
        for key, category in categories.items():
            if key in question:
                filtered_df = filtered_df[filtered_df['category'] == category]
                category_used = category
                break
        
        # Apply brand filter if mentioned
        brand_used = None
        for brand in brands:
            if brand in question:
                filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
                brand_used = brand.title()
                break
        
        if filtered_df.empty:
            return "❌ No products found matching your criteria."
        
        # Find most expensive in filtered data
        max_price_idx = filtered_df['price'].idxmax()
        product = filtered_df.loc[max_price_idx]
        
        # Generate context-aware response
        context = ""
        if category_used:
            context = f" {category_used.lower()}"
        if brand_used:
            context = f" {brand_used}"
        if category_used and brand_used:
            context = f" {brand_used} {category_used.lower()}"
        
        return f"💰 Most Expensive{context} Watch: {product['product_name']} - ₹{product['price']:,} (Rating: {product['rating']}⭐)"

    def find_cheapest(self, question):
        # Similar logic to find_most_expensive but for cheapest
        filtered_df = self.df
        
        categories = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury', 
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital',
            'analog': 'Analog'
        }
        
        brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
        
        # Apply category filter if mentioned
        category_used = None
        for key, category in categories.items():
            if key in question:
                filtered_df = filtered_df[filtered_df['category'] == category]
                category_used = category
                break
        
        # Apply brand filter if mentioned
        brand_used = None
        for brand in brands:
            if brand in question:
                filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
                brand_used = brand.title()
                break
        
        if filtered_df.empty:
            return "❌ No products found matching your criteria."
        
        min_price_idx = filtered_df['price'].idxmin()
        product = filtered_df.loc[min_price_idx]
        
        # Generate context-aware response
        context = ""
        if category_used:
            context = f" {category_used.lower()}"
        if brand_used:
            context = f" {brand_used}"
        if category_used and brand_used:
            context = f" {brand_used} {category_used.lower()}"
        
        return f"💸 Cheapest{context} Watch: {product['product_name']} - ₹{product['price']:,} (Rating: {product['rating']}⭐)"

    def filter_by_max_price(self, question):
        # specified price
        numbers = re.findall(r'[\d.]+', question)
        if not numbers:
            return "Please specify a price (e.g., 'watches under 10000')"

        max_price = float(numbers[0])
        affordable_items = self.df[self.df['price'] <= max_price]

        if affordable_items.empty:
            return f"No watches found under ₹{max_price:,}"

        results = "\n".join([
            f"{row['product_name']} - ₹{row['price']:,} (Rating: {row['rating']})"
            for _, row in affordable_items.head(8).iterrows()
        ])
        return f"🛍️ Watches under ₹{max_price:,}:\n{results}"

   # rating and review analysis
    def filter_by_rating(self, question):
        numbers = re.findall(r'[\d.]+', question)
        if not numbers:
            return "Please specify a rating threshold (e.g., 'rating above 4.5')"

        threshold = float(numbers[0])
        high_rated = self.df[self.df['rating'] > threshold]

        if high_rated.empty:
            return f"No watches found with rating above {threshold}"

        results = "\n".join([
            f"⭐ {row['product_name']} - ₹{row['price']:,} (Rating: {row['rating']})"
            for _, row in high_rated.head(8).iterrows()
        ])
        return f"Watches with rating above {threshold}:\n{results}"

    def find_most_reviews(self, question):
        """Find the product with the most reviews with context."""
        filtered_df = self.df
        
        categories = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury', 
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital',
            'analog': 'Analog'
        }
        
        brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
        
        # Apply category filter if mentioned
        category_used = None
        for key, category in categories.items():
            if key in question:
                filtered_df = filtered_df[filtered_df['category'] == category]
                category_used = category
                break
        
        # Apply brand filter if mentioned
        brand_used = None
        for brand in brands:
            if brand in question:
                filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
                brand_used = brand.title()
                break
        
        if filtered_df.empty:
            return "❌ No products found matching your criteria."
        
        max_reviews_idx = filtered_df['reviews'].idxmax()
        product = filtered_df.loc[max_reviews_idx]
        
        # Generate context-aware response
        context = ""
        if category_used:
            context = f" {category_used.lower()}"
        if brand_used:
            context = f" {brand_used}"
        if category_used and brand_used:
            context = f" {brand_used} {category_used.lower()}"
        
        return f"📝 Most Reviews{context}: {product['product_name']} - {product['reviews']:,} reviews (Rating: {product['rating']}⭐)"

    # category and brand analysis
    def calculate_average_price(self, question):
        category_map = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury',
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital'
        }

        for key, category in category_map.items():
            if key in question:
                avg_price = self.df[self.df['category'] == category]['price'].mean()
                return f"Average price of {category.lower()} watches: ₹{avg_price:,.2f}"

        overall_avg = self.df['price'].mean()
        return f"📊 Average price of all watches: ₹{overall_avg:,.2f}"

    def category_analysis(self, question):
        categories = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury',
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital',
            'analog': 'Analog'
        }

        results = []
        for key, name in categories.items():
            if key in question:
                subset = self.df[self.df['category'] == name]
                if not subset.empty:
                    avg_price = subset['price'].mean()
                    avg_rating = subset['rating'].mean()
                    results.append(f"{name}: {len(subset)} watches, Avg ₹{avg_price:,.2f}, Rating {avg_rating:.1f}⭐")

        return "\n".join(results) if results else "I can analyze: smartwatch, luxury, sports, fashion, digital, or analog watches."

    def brand_analysis(self, question):
        # summarization of brands 
        brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
        results = []

        for brand in brands:
            if brand in question:
                subset = self.df[self.df['brand'].str.lower().str.contains(brand)]
                if not subset.empty:
                    avg_price = subset['price'].mean()
                    avg_rating = subset['rating'].mean()
                    results.append(f"{brand.title()}: {len(subset)} watches, Avg ₹{avg_price:,.2f}, Rating {avg_rating:.1f}⭐")

        return "\n".join(results) if results else "Try: Titan, Casio, Fastrack, Sonata, Fossil, Samsung, Apple, or Noise."


    def show_price_range(self, question):
        """Show price range with optional filtering"""
        filtered_df = self.df
        
        categories = {
            'smartwatch': 'Smartwatch',
            'luxury': 'Luxury', 
            'sports': 'Sports',
            'fashion': 'Fashion',
            'digital': 'Digital',
            'analog': 'Analog'
        }
        
        brands = ['titan', 'casio', 'fastrack', 'sonata', 'fossil', 'samsung', 'apple', 'noise']
        
        # Apply category filter if mentioned
        category_used = None
        for key, category in categories.items():
            if key in question:
                filtered_df = filtered_df[filtered_df['category'] == category]
                category_used = category
                break
        
        # Apply brand filter if mentioned
        brand_used = None
        for brand in brands:
            if brand in question:
                filtered_df = filtered_df[filtered_df['brand'].str.lower().str.contains(brand)]
                brand_used = brand.title()
                break
        
        if filtered_df.empty:
            return "❌ No products found matching your criteria."
        
        min_price = filtered_df['price'].min()
        max_price = filtered_df['price'].max()
        
        context = ""
        if category_used:
            context = f" for {category_used.lower()} watches"
        if brand_used:
            context = f" for {brand_used} watches"
        if category_used and brand_used:
            context = f" for {brand_used} {category_used.lower()} watches"
        
        return f"📈 Price Range{context}: ₹{min_price:,} - ₹{max_price:,}"

    def show_categories(self):
        # counts and averages
        category_counts = self.df['category'].value_counts()
        result = ["Watch Categories:"]
        for category, count in category_counts.items():
            avg_price = self.df[self.df['category'] == category]['price'].mean()
            result.append(f"• {category}: {count} watches (Avg ₹{avg_price:,.2f})")
        return "\n".join(result)

    def show_help(self):
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

# main program
def main():
    # chatbot
    try:
        bot = ProductInsightBot()

        while True:
            user_input = input("\nYour question: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thank you for using ProductInsightBot!")
                break

            try:
                answer = bot.analyze_query(user_input)
                print(f"\n💡 {answer}")
            except Exception as e:
                print(f"❌ Error processing your question: {e}")

    except FileNotFoundError:
        print("❌ Products data not found. Please make sure 'products.csv' exists!")

if __name__ == "__main__":
    main()