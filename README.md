## ProductInsightBot
ProductInsightBot is an intelligent AI agent designed to analyze and provide insights about watch products. 

## **Demo** - https://product-insight-bot.vercel.app/
https://github.com/user-attachments/assets/8e071a75-c3ae-47c8-a42b-98f70a0ab690


## **Features**
- **Web Scraping**: Automated data collection from e-commerce websites
- **Natural Language Processing**: Understands conversational queries about watches
- **Price Analysis**: Compares prices, finds expensive/affordable watches
- **Rating Filtering**: Filters products by customer ratings
- **Brand Comparison**: Analyzes and compares different watch brands
- **Category Insights**: Provides insights across Smartwatch, Luxury, Sports, Fashion, Digital, and Analog categories

## **Technologies Used**
- **Python 3.x** - Core programming language
- **Pandas** - Data manipulation and analysis
- **BeautifulSoup4** - Web scraping and HTML parsing
- **Requests** - HTTP requests for web scraping
- **SQLite** - Database storage
- **Regular Expressions** - Natural language pattern matching

## **Project Structure**
<img width="683" height="252" alt="image" src="https://github.com/user-attachments/assets/a95de79b-6613-4eac-84d1-3fa020564fc9" />

## **Installation & Setup**

### _Prerequisites_
- Python 3.7 or higher
- pip (Python package manager)

### _Step 1: Clone the Repository_
```bash
git clone https://github.com/GurmanpreetKaur23/ProductInsightBot.git
cd ProductInsightBot
```
### _Step 2: Install Dependencies_
``` bash
pip install -r requirements.txt
```
### _Step 3: Generate Product Data_
``` bash
python data_collector.py
```
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/5190813a-dab7-4405-ae1d-17aaed25981a" />

### _Step 4: Run the AI Agent_
``` bash
python product_insight_bot.py
```
<img width="1597" height="467" alt="image" src="https://github.com/user-attachments/assets/acf8f673-0d88-4fa1-98ae-de6d91ee3a8e" />

## **Usage Examples**
<img width="1601" height="894" alt="image" src="https://github.com/user-attachments/assets/7877c938-a221-4dc9-8e29-1c630a2caff4" />

## **Data Collection Approach**

### _Web Scraping Strategy_
**-> Attempts to scrape real watch data from Amazon India**

**-> Implements respectful scraping with delays between requests**

**-> Uses proper headers to mimic browser behavior**

**-> Handles errors gracefully with fallback mechanisms**

### _Fallback Data Generation_
**-> Generates realistic sample data if scraping fails**

**-> Includes 200+ watch products across 6 categories**

**-> Realistic pricing, ratings, and review counts**

**-> Covers popular brands like Titan, Casio, Apple, Samsung, etc.**

### **Categories Covered**
<img width="810" height="425" alt="image" src="https://github.com/user-attachments/assets/6f90da4e-f385-41b8-9df3-fed125ca7288" />

### **Technical Implementation**
## _Data Collection_ _**(data_collector.py)**_
**-> Web scraping with error handling**

**-> Automatic category classification**

**-> Brand extraction from product names**

**-> CSV and SQLite database storage**

## _AI Agent_ _**(product_insight_bot.py)**_
**-> Pattern-based natural language understanding**

**-> Category and brand recognition**

**-> Statistical analysis and filtering**

**-> User-friendly conversational interface**

### **Troubleshooting**
## _Common Issues_
**Web scraping fails:** The system automatically uses generated sample data

**Module not found:** Run pip install -r requirements.txt

**Database errors:** Delete products.db and run data_collector.py again

##_Data Sources_
**Primary:** Amazon India (web scraping)

**Fallback:** Generated sample data with realistic watch information
