import pandas as pd
import os

class DataProcessor:
    def __init__(self, sep=';', directory=None):
        """
        Initialize the MediaDataProcessor with a separator and directory.
        
        Args:
            sep (str): The separator used in the CSV files. Defaults to ';'.
            directory (str): The directory where the CSV files are located. Defaults to the current directory.
        """
        self.sep = sep
        self.directory = directory
        self.df_merged = None

    def get_csv(self):
        """
        Reads and merges the first two CSV files in the specified directory.

        Returns:
            pd.DataFrame: The merged DataFrame.
        """
        # List CSV files in the directory
        csv_files = [f for f in os.listdir(self.directory) if f.endswith('.csv')]

        if len(csv_files) < 2:
            raise ValueError("At least two CSV files are required for merging.")

        # Read the first two CSV files into DataFrames
        df1 = pd.read_csv(os.path.join(self.directory, csv_files[0]), sep=self.sep)
        df2 = pd.read_csv(os.path.join(self.directory, csv_files[1]), sep=self.sep)

        # Merge the DataFrames on specified columns
        self.df_merged = df1.merge(df2, on=['P8_ID', 'P8_MBA_A_Haushalt'])

        return self.df_merged

    def calculations(self, student=0):
        """
        Performs calculations on the merged DataFrame based on the student flag.

        Args:
            student (int): Flag indicating if the condition is student (1) or not (0). Defaults to 0.

        Returns:
            pd.DataFrame: The DataFrame with additional columns calculated.
        """
        if self.df_merged is None:
            raise ValueError("The DataFrame is not loaded. Please call 'get_csv()' first.")
        
        # Ensure 'student' is an integer (0 or 1)
        if student not in [0, 1]:
            raise ValueError("The 'student' parameter should be 0 or 1.")

        # Compute 'apx_population'
        self.df_merged['apx_population'] = self.df_merged['P8_MBA_A_Haushalt'] * 2

        # Compute 'estimated_target_population'
        if student == 1:
            self.df_merged['estimated_target_population'] = self.df_merged['apx_population'] * self.df_merged['P8_B4P_P_STUDENTEN'] / 100
        else:
            self.df_merged['estimated_target_population'] = self.df_merged['apx_population'] * self.df_merged['P8_B4P_P_ALTER_18_29']/100
        return self.df_merged