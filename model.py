import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os

def train_optimization_model():
    file_name = 'nassu_data.csv'
    
    # Read actual CSV file if available, otherwise use fallback data
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            
            # Map or create columns safely from CSV data
            if 'Distance' not in df.columns:
                df['Distance'] = np.random.randint(50, 1500, len(df))
            if 'Quantity' not in df.columns and 'Units' in df.columns:
                df['Quantity'] = df['Units']
            elif 'Quantity' not in df.columns:
                df['Quantity'] = np.random.randint(100, 5000, len(df))
            if 'Cost' not in df.columns:
                df['Cost'] = np.random.randint(500, 5000, len(df))
            if 'LeadTime' not in df.columns:
                df['LeadTime'] = np.random.uniform(1, 10, len(df))
                
            df['Factory_Encoded'] = np.random.randint(0, 5, len(df))
            df['Category_Encoded'] = np.random.randint(0, 3, len(df))
            df['Urgency'] = np.random.randint(1, 4, len(df))
            
        except Exception as e:
            df = create_dummy_dataframe()
    else:
        df = create_dummy_dataframe()
        
    X = df[['Factory_Encoded', 'Category_Encoded', 'Distance', 'Quantity', 'Urgency']]
    y_cost = df['Cost']
    y_time = df['LeadTime']
    
    cost_model = RandomForestRegressor(n_estimators=50, random_state=42)
    cost_model.fit(X, y_cost)
    
    time_model = RandomForestRegressor(n_estimators=50, random_state=42)
    time_model.fit(X, y_time)
    
    return cost_model, time_model

def create_dummy_dataframe():
    n_samples = 500
    return pd.DataFrame({
        'Factory_Encoded': np.random.randint(0, 5, n_samples),
        'Category_Encoded': np.random.randint(0, 3, n_samples),
        'Distance': np.random.randint(50, 1500, n_samples),
        'Quantity': np.random.randint(100, 5000, n_samples),
        'Urgency': np.random.randint(1, 4, n_samples),
        'Cost': np.random.randint(500, 5000, n_samples),
        'LeadTime': np.random.uniform(1, 10, n_samples)
    })

def predict_shipping_portal(factory_idx, cat_idx, distance, quantity, urgency):
    cost_model, time_model = train_optimization_model()
    input_data = np.array([[factory_idx, cat_idx, distance, quantity, urgency]])
    
    pred_cost = cost_model.predict(input_data)[0]
    pred_time = time_model.predict(input_data)[0]
    
    return round(pred_cost, 2), round(pred_time, 1)