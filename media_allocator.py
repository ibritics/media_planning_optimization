# media_allocator.py

import pandas as pd

class MediaAllocator:
    def __init__(self, df, total_budget, CPM):
        self.df = df.copy()
        self.total_budget = total_budget
        self.CPM = CPM
        self.allocated_budget = 0
        self.allocation = []
        self.total_target_reach = 0
        self.max_reach = self.total_budget / self.CPM * 1000

    def filter_rows(self):
        # Step 1: Filter rows where apx_population is within reach capacity
        self.df['within_reach'] = self.df['apx_population'] <= self.max_reach

        # Step 3: Filter the dataframe to include only those rows within reach capacity
        self.df_filtered = self.df[self.df['within_reach']].sort_values(by='estimated_target_population', ascending=False)

    def allocate_budget(self):
        # Keep processing as long as there is budget and rows left in the DataFrame
        while self.total_budget > 0 and not self.df_filtered.empty:
            new_allocation = []
            print(f"New Allocation Starts, Remaining Budget: {self.total_budget}")
            print(self.df_filtered[['P8_ID', 'apx_population', 'estimated_target_population']])

            # Iterate over the rows and allocate budget
            for index, row in self.df_filtered.iterrows():
                impressions_needed = row['apx_population']
                cost_needed = impressions_needed / 1000 * self.CPM
                print(f"Processing P8_ID {row['P8_ID']}: Impressions Needed = {impressions_needed}, Cost Needed = {cost_needed}, Remaining Budget = {self.total_budget}")

                if cost_needed <= self.total_budget:
                    print('Allocation Possible')
                    new_allocation.append((row['P8_ID'], cost_needed, row['estimated_target_population']))
                    self.total_target_reach += row['estimated_target_population']
                    self.allocated_budget += cost_needed
                    self.total_budget -= cost_needed
                    print(f"Updated Budget After Allocation: {self.total_budget}")

            # Append new allocations to the overall allocation list
            self.allocation.extend(new_allocation)

            # Update df_filtered for the new total_budget to consider smaller populations
            self.df_filtered = self.df_filtered[self.df_filtered['apx_population'] <= (self.total_budget / self.CPM) * 1000]

            print(f"Filtered df based on remaining budget: {self.total_budget}")
            print(self.df_filtered[['P8_ID', 'apx_population', 'estimated_target_population']])

            # If no new allocation was possible in this loop iteration, break the loop
            if not new_allocation:
                print("No further allocation possible, breaking loop.")
                break

    def get_results(self):
        # Return the final allocation, total target reach, and remaining budget
        results = {
            'final_allocation': self.allocation,
            'total_target_reach': self.total_target_reach,
            'remaining_budget': self.total_budget
        }
        
        # Convert the allocation results to a DataFrame
        allocation_df = pd.DataFrame(results['final_allocation'], columns=['ID', 'Amount', 'Reach'])
        
        # Create a summary DataFrame for the total_target_reach and remaining_budget
        summary_df = pd.DataFrame({
            'Total Target Reach': [results['total_target_reach']],
            'Remaining Budget': [results['remaining_budget']]
        })
        
        return allocation_df, summary_df