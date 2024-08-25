from dash import Dash, html, dcc, Input, Output, dash_table, State
import pandas as pd
from data_preprocessing import DataProcessor
from media_allocator import MediaAllocator
import os

# Initialize the DataProcessor and load the CSV
my_path = os.getcwd()
processor = DataProcessor(directory=my_path)
input_file = processor.get_csv()

app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
        # Header with image
        html.Div(
            [
                html.Img(
                    src='/assets/logo.png',  # Ensure your PNG is correctly placed in the 'assets' folder
                    style={'height': '60px', 'width': 'auto', 'display': 'block', 'margin-right': '20px'}
                ),
                html.H4("Media Allocation Table", style={"textAlign": "center", "margin": 30}),
            ],
            style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}
        ),
        
        # Budget Input
        html.Label("Budget", htmlFor="budget-input"),
        dcc.Input(id="budget-input", type="number", value=1000, step=100),
        
        # CPM Input
        html.Label("CPM", htmlFor="CPM-input"),
        dcc.Input(id="CPM-input", type="number", value=10, step=1),

        # Student Switch
        html.Label("Student", htmlFor="student-switch"),
        dcc.RadioItems(
            id="student-switch",
            options=[
                {"label": "Yes", "value": 1},
                {"label": "No", "value": 0},
            ],
            value=0,  # Default is "No"
            labelStyle={'display': 'flex', 'align-items': 'right', 'margin-bottom': '20px'}
        ),
        
        # Button to Run Allocation
        html.Button('Run Allocation', id='run-button', n_clicks=0),
        
        # Separate DataTables for Allocation and Summary
        html.Div(
            [
                html.H5("Allocation Table"),
                dash_table.DataTable(
                    id="allocation-table",
                    page_size=10,
                ),
                html.H5("Summary Table"),
                dash_table.DataTable(
                    id="summary-table",
                    page_size=10,
                )
            ],
            style={"margin-top": 20}
        )
    ], style={"margin": 20}
)

@app.callback(
    [Output("allocation-table", "data"),
     Output("summary-table", "data")],
    [
        Input("run-button", "n_clicks")
    ],
    [
        State("budget-input", "value"),
        State("CPM-input", "value"),
        State("student-switch", "value")
    ]
)
def update_tables(n_clicks, budget, CPM, student):
    if n_clicks > 0:
        # Perform calculations
        processed_df = processor.calculations(student=student)
        
        # Initialize MediaAllocator with the updated DataFrame and inputs
        allocator = MediaAllocator(df=processed_df, total_budget=budget, CPM=CPM)
        
        # Filter rows and allocate budget
        allocator.filter_rows()
        allocator.allocate_budget()
        
        # Get results and convert to DataFrames
        allocation_df, summary_df = allocator.get_results()
        
        # Return updated data for both DataTables
        return allocation_df.to_dict("records"), summary_df.to_dict("records")
    
    # Return empty tables if button hasn't been clicked
    return [], []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
