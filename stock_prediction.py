import os
import pandas as pd
import random
from datetime import datetime, timedelta

def output_file_exists(file_path):
    return os.path.exists(file_path)


# Constants
INPUT_DIR = "./data/input"  # Path to the folder containing stock exchange folders
OUTPUT_DIR = "./output/input"  # Path to save output CSV files
NUM_FILES = 2  # Recommended number of files to sample per stock exchange

# Helper function to parse timestamps
def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, "%d-%m-%Y")

# Helper function to format timestamps
def format_timestamp(timestamp):
    return timestamp.strftime("%d-%m-%Y")

# Function 1: Data Sampler
def sample_data(file_path):
    try:
        # Read the CSV file and specify column names manually
        data = pd.read_csv(file_path, header=None, names=['Stock-ID', 'Timestamp', 'Stock Price'])
        
        # Convert the "Timestamp" column to datetime
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d-%m-%Y')
        
        # Ensure there are at least 10 rows to sample
        if len(data) < 10:
            raise ValueError(f"Not enough data points in file: {file_path}")
        
        # Randomly select a starting index for 10 consecutive rows
        start_index = random.randint(0, len(data) - 10)
        sampled_data = data.iloc[start_index:start_index + 10].copy()
        return sampled_data
    
    except Exception as e:
        print(f"Error in sampling data from {file_path}: {e}")
        return None

# Function 2: Predictor
def predict_next_values(sampled_data):
    try:
        stock_id = sampled_data['Stock-ID'].iloc[0]
        timestamps = sampled_data['Timestamp'].tolist()
        prices = sampled_data['Stock Price'].tolist()

        # Prediction logic
        n = prices[-1]
        n_plus_1 = sorted(prices)[-2]  # 2nd highest value
        n_plus_2 = n + (n_plus_1 - n) / 2
        n_plus_3 = n_plus_2 + (n_plus_1 - n_plus_2) / 4

        # Generate new timestamps
        last_timestamp = timestamps[-1]
        next_timestamps = [last_timestamp + timedelta(days=i) for i in range(1, 4)]

        # Prepare output data
        predictions = [
            [stock_id, format_timestamp(next_timestamps[0]), n_plus_1],
            [stock_id, format_timestamp(next_timestamps[1]), n_plus_2],
            [stock_id, format_timestamp(next_timestamps[2]), n_plus_3],
        ]
        return predictions
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

# Main Processing Function
def process_stock_exchange(exchange_folder):
    exchange_path = os.path.join(INPUT_DIR, exchange_folder)
    if not os.path.isdir(exchange_path):
        print(f"Directory not found: {exchange_path}")
        return

    output_path = os.path.join(OUTPUT_DIR, exchange_folder)
    os.makedirs(output_path, exist_ok=True)

    files = [f for f in os.listdir(exchange_path) if f.endswith('.csv')]
    files_to_process = files[:NUM_FILES]

    for file_name in files_to_process:
        file_path = os.path.join(exchange_path, file_name)
        sampled_data = sample_data(file_path)

        if sampled_data is not None:
            predictions = predict_next_values(sampled_data)

            if predictions is not None:
                output_file_path = os.path.join(output_path, file_name)
                sampled_data['Timestamp'] = sampled_data['Timestamp'].apply(format_timestamp)
                sampled_data = sampled_data[['Stock-ID', 'Timestamp', 'Stock Price']]
                prediction_df = pd.DataFrame(predictions, columns=['Stock-ID', 'Timestamp', 'Stock Price'])
                result = pd.concat([sampled_data, prediction_df])
                result.to_csv(output_file_path, index=False)
                print(f"Processed and saved: {output_file_path}")

for exchange in os.listdir(INPUT_DIR):
    exchange_dir = os.path.join(INPUT_DIR, exchange)
    if not os.path.isdir(exchange_dir):
        continue

    for input_file in os.listdir(exchange_dir):
        input_file_path = os.path.join(exchange_dir, input_file)

        # Generate the corresponding output file path
        output_file_path = os.path.join(
            OUTPUT_DIR,
            exchange,
            input_file  # Use the same name as input file
        )

        # Ensure the output directory exists
        output_file_dir = os.path.dirname(output_file_path)
        os.makedirs(output_file_dir, exist_ok=True)

        # Check if the output file already exists
        if output_file_exists(output_file_path):
            print(f"Output file already exists for {input_file_path}. Skipping processing.")
            continue

        # Process the file (sample data, predict values, and save output)
        sampled_data = sample_data(input_file_path)
        if sampled_data is None:
            continue  # Skip if sampling failed

        # Function to save predictions to the output file
def save_predictions(output_file_path, sampled_data, predictions):
    try:
        if predictions is not None:
            sampled_data['Timestamp'] = sampled_data['Timestamp'].apply(format_timestamp)
            sampled_data = sampled_data[['Stock-ID', 'Timestamp', 'Stock Price']]
            prediction_df = pd.DataFrame(predictions, columns=['Stock-ID', 'Timestamp', 'Stock Price'])
            result = pd.concat([sampled_data, prediction_df])
            result.to_csv(output_file_path, index=False)
            print(f"Predictions saved successfully to {output_file_path}")
        else:
            print("No predictions to save.")
    except Exception as e:
        print(f"Error saving predictions to {output_file_path}: {e}")

        predictions = predict_next_values(sampled_data)
        save_predictions(output_file_path, sampled_data, predictions)
        print(f"Processed and saved output for {input_file_path}.")
                

# Main Script
def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    exchanges = [d for d in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, d))]

    for exchange in exchanges:
        process_stock_exchange(exchange)

if __name__ == "__main__":
    main()