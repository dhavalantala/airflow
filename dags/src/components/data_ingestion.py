import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_insurance_data():
    """Fetches insurance data, splits it, and saves it to artifacts."""
    url = "https://raw.githubusercontent.com/dhavalantala/Vehicle-Insurance/refs/heads/main/notebook/data.csv"
    
    # Use the absolute path mapped to your local computer
    artifacts_dir = "/opt/airflow/artifacts"
    
    try:
        # Load data
        df = pd.read_csv(url, sep=';')
        
        # Create artifacts directory
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # Split data
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
        
        # Save splits to the mapped folder path
        train_set.to_csv(os.path.join(artifacts_dir, "train.csv"), index=False, sep=';')
        test_set.to_csv(os.path.join(artifacts_dir, "test.csv"), index=False, sep=';')
        
        print("Data successfully split and saved to artifacts folder.")
        return "Data splitting successful"
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e
