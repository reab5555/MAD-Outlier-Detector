import pandas as pd
import numpy as np
import gradio as gr


def calculate_mad_outliers(data, threshold=3.2):
    """Calculate outliers using Median Absolute Deviation (MAD)"""
    try:
        numeric_data = pd.to_numeric(data, errors='coerce')

        if numeric_data.isna().all():
            return None, "Error: No numeric data to process"

        median = np.median(numeric_data[numeric_data.notna()])
        mad = np.median(np.abs(numeric_data[numeric_data.notna()] - median))
        if mad == 0:
            return None, "Error: MAD is zero, cannot process"

        modified_zscore = 0.6745 * (numeric_data - median) / mad
        outliers = abs(modified_zscore) > threshold
        return outliers, None
    except Exception as e:
        return None, f"Error processing data: {str(e)}"


def update_columns(file):
    if file is None:
        return gr.update(choices=[]), gr.update(choices=[])
    df = pd.read_csv(file.name)
    columns = df.columns.tolist()
    return gr.update(choices=columns), gr.update(choices=columns)


def process_file(file, index_column, values_column):
    """Process the CSV file and remove outliers"""
    try:
        df = pd.read_csv(file.name)

        if index_column not in df.columns or values_column not in df.columns:
            return None, "Selected columns not found in dataset"

        outliers, error = calculate_mad_outliers(df[values_column])
        if error:
            return None, error

        outliers_df = df[outliers]

        if len(outliers_df) == 0:
            return None, "No outliers found in the values"

        cleaned_df = df[~outliers]

        # Save cleaned file
        cleaned_path = "cleaned_data.csv"
        cleaned_df.to_csv(cleaned_path, index=False)

        summary = f"""
        Total rows: {len(df)}
        Outliers found: {len(outliers_df)}
        Remaining rows: {len(cleaned_df)}

        Outliers detected:
        {outliers_df[[index_column, values_column]].to_string()}
        """

        return cleaned_path, summary

    except Exception as e:
        return None, f"Error: {str(e)}"


def create_interface():
    with gr.Blocks(title="Outlier Detector") as iface:
        gr.Markdown("# Outlier Detector using MAD method")

        with gr.Row():
            file_input = gr.File(label="Upload CSV file", file_types=[".csv"])

        with gr.Row():
            index_column = gr.Dropdown(label="Index Column", choices=[], interactive=True)
            values_column = gr.Dropdown(label="Values Column", choices=[], interactive=True)

        with gr.Row():
            process_button = gr.Button("Process and Remove Outliers")

        output_text = gr.Textbox(label="Results", lines=10)

        with gr.Row():
            cleaned_file = gr.File(label="Download Cleaned CSV")


        # Update dropdown options when file is uploaded
        file_input.change(
            fn=update_columns,
            inputs=[file_input],
            outputs=[index_column, values_column]
        )

        process_button.click(
            fn=process_file,
            inputs=[file_input, index_column, values_column],
            outputs=[cleaned_file, output_text]
        )

    return iface


if __name__ == "__main__":
    iface = create_interface()
    iface.launch(share=False)