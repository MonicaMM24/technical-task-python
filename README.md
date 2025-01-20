# technical-task-python
Simple application to predict values of stock price

The script processes CSV files containing stock price data, samples a subset of the data, predicts the next three stock prices using a simple algorithm, and saves the results in an output file.
/data/input/ contains folders for each stock exchange, each containing CSV files with historical stock price data.
/output/ is where the predicted data will be saved. This folder is automatically created if it doesn't exist.

# Prerequisites  
-clone this repository

-make sure you have Python installed (python 3.13 was used in the project)

-run the command pip install pandas to install the dependencies

# How to Run
Prepare the input data: Place the historical stock price CSV files in the /data/input/ directory. Each CSV file should contain data in the following format:

Stock-ID: A unique identifier for the stock.
Timestamp: Date in the format dd-mm-yyyy.
Stock Price: The closing price of the stock on that day.

Run the script: Once the data is prepared, you can run the Python script main.py to process the input files and generate predictions. The script will automatically create the necessary output directories and save the results.

Check the output: After running the script, you will find the predicted stock prices saved in the /output/input/ directory. The output files will be named the same as the input files and will contain both the sampled data and the predicted values for the next three days.

# Output Format
Each output file will have the following columns:

Stock-ID: The identifier for the stock.
Timestamp: The date of the stock price (in dd-mm-yyyy format).
Stock Price: The predicted stock price.
