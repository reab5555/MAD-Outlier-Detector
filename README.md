# MAD Outlier Detector

This is a Python tool built using `pandas`, `numpy`, and `gradio` that detects and removes outliers from a dataset using the Median Absolute Deviation (MAD) technique. It's designed to be user-friendly and provides a clear summary of the results.

## Features

-   **CSV File Upload**: Upload your dataset in CSV format.
-   **Column Selection**: Choose which columns to use as the index and the column containing the values to analyze.
-   **Robust MAD Outlier Detection**: Implements the Median Absolute Deviation (MAD) method, which is more robust to outliers than methods based on mean and standard deviation.
-   **Outlier Removal**: Creates a cleaned version of your dataset with the detected outliers removed.
-   **Detailed Summary**:  Provides a summary including:
    -   The total number of rows in the original dataset.
    -   The number of outliers detected.
    -   The number of rows in the cleaned dataset.
    -   A display of the actual detected outliers and their index and value columns.
-   **Cleaned File Download**: Download the cleaned dataset as a new CSV file.
-   **Interactive Web Interface**: Built with `gradio` for an easy and intuitive user experience.

## How It Works (Based on Median Absolute Deviation - MAD)

This tool uses the MAD method, a robust statistical measure, to identify outliers in a single data column of a dataset.  Here's a breakdown of the process:

1.  **Data Type Handling**: The tool first attempts to convert the selected column of your data to a numeric format. Non-numeric data will be coerced to `NaN` (Not a Number).
2.  **Median Calculation:** The median value of the selected column data is computed. Since median is robust to outliers is preferred against the mean.
3.  **Median Absolute Deviation (MAD) Calculation**: The absolute difference between each data point and the median is calculated. Then the median of these absolute deviations is taken.
    -   *Formula:* MAD =  median(|xi - median(x)|)
4. **Zero MAD Handling**: If the MAD is zero, which can happen if all values are the same, the tool will stop processing because the next step will lead to a division by zero.
5.  **Modified Z-Score Calculation:** The "Modified Z-score" of each data point is calculated. 
    -  *Formula:* Modified Z-score = 0.6745 * (xi - median(x)) / MAD
6.  **Outlier Identification**: Data points with an absolute modified Z-score above a predefined *threshold* are considered outliers. The default threshold is 3.2 which is close to the critical value for p <.001 (as shown in the article).
7. **Data Cleaning**: All rows that contain an outlier will be removed, and the cleaned dataset will be available for download.

## Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd mad-outlier-detector
    ```
2.  **Install Dependencies**:
    ```bash
    pip install pandas numpy gradio
    ```
3.  **Run the Application**:
    ```bash
    python app.py
    ```
4.  Open your web browser and navigate to the URL provided by the console.

## Usage

1.  **Upload CSV**: Use the provided "Upload CSV file" component to upload your CSV data.
2.  **Select Columns**: Select the desired "Index Column" and "Values Column" from the dropdowns.
3.  **Process Data**: Click the "Process and Remove Outliers" button to perform outlier detection.
4.  **View Results**: The "Results" textbox will display the summary of the process, number of outliers, and remaining rows. It will also print the detected outliers.
5.  **Download Cleaned File**: Click the "Download Cleaned CSV" button to download the new cleaned file.

## Dependencies

-   pandas
-   numpy
-   gradio
