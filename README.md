-----

# 🤖 HackerEarth Leaderboard Scraper

Ever wanted to grab the leaderboard data from a competitive programming contest on HackerEarth? This tool does exactly that\! Simply enter the name of a contest, and this web app will scrape the leaderboard, display it in a clean table, and even let you download the results as a CSV file.


----- <img width="2511" height="1240" alt="Screenshot 2025-07-30 032556" src="https://github.com/user-attachments/assets/4915bfc0-381a-4402-944b-2745326eb0d7" />


## ✨ Features

  * **Simple Web Interface**: No complex commands needed. Just open the web page and type in a contest name.
  * **Dynamic Scraping**: Uses Selenium to pull live leaderboard data directly from the HackerEarth website.
  * **Interactive Results Table**: The scraped data is displayed in a clean, filterable table on the results page.
  * **Live Filtering**: Instantly filter the results by any column (Rank, Name, Score, etc.) without reloading the page.
  * **Download as CSV**: With a single click, download the complete leaderboard data for your own analysis.

-----

## 🔧 How It Works

This project is a **Flask** web application that uses **Selenium** in the background to control a headless Chrome browser. When you submit a contest name, the following happens:

1.  **Flask Backend**: Receives the request from the frontend.
2.  **Selenium Scraper**: Navigates through the leaderboard pages on HackerEarth, scraping the data from each row.
3.  **Data Parsing**: The raw data is parsed and structured into a clean format.
4.  **Render Results**: The data is sent back to the user's browser and displayed in an HTML table.
5.  **Download Request**: If you click the download button, the app re-scrapes the data and sends it back as a CSV file attachment.

-----

## 🚀 Getting Started

To get this project running on your local machine, follow these simple steps.

### **Prerequisites**

  * Python 3.x
  * Google Chrome browser installed
  * ChromeDriver (make sure its version matches your Google Chrome version)

### **Installation**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/hackerearth-scraper.git
    cd hackerearth-scraper
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

### **Running the Application**

1.  **Execute the `app.py` script:**

    ```bash
    python app.py
    ```

2.  **Open your web browser** and navigate to:
    [http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000)

-----

## 🛠️ Technologies Used

  * **Backend**: Flask
  * **Web Scraping**: Selenium
  * **Frontend**: HTML, CSS, JavaScript
  * **Language**: Python
