from utils import Dashboard
import pandas as pd

# Load and prepare the CSV
df = pd.read_csv("Data/updated_data.csv")
rename_dict_GAds = {'GAds-Cost Per Click': 'Cost Per Click', 'GAds-Cost Per Lead': 'Cost Per Lead', 'GAds-Click Through Rate': 'Click Through Rate', 'GAds-Conversion Rate': 'Conversion Rate', 'GAds-Average ROAS': 'Average ROAS'}
rename_dict_Meta = {'Meta-Cost Per Click': 'Cost Per Click', 'Meta-Cost Per Lead': 'Cost Per Lead', 'Meta-Click Through Rate': 'Click Through Rate', 'Meta-Conversion Rate': 'Conversion Rate', 'Meta-Average ROAS': 'Average ROAS'}

df_1 = df[['Industry'] + list(rename_dict_GAds.keys())].rename(columns=rename_dict_GAds)
df_2 = df[['Industry'] + list(rename_dict_Meta.keys())].rename(columns=rename_dict_Meta)

# Coefficient of Variation Dictionary
CV_dict = {'Cost Per Click': 0.5097, 'Cost Per Lead': 0.5097, 'Click Through Rate': 0.3965, 'Conversion Rate': 0.6629, 'Average ROAS': 0.4904}

# Initialize the dashboard
Dash = Dashboard(df_1, df_2, CV_dict)
Dash.get_dashboard().servable().show()