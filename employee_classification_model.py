import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
# Replace 'updated_dataset.csv' with the actual path to your dataset
df = pd.read_csv("C:/Users/Administrator/Desktop/updated_dataset.csv")

# Define features (X) and target (y)
X = df.drop(columns=['Mental_Health_Condition'])  # 'Type' is the target column
y = df['Mental_Health_Condition']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model to a file
joblib.dump(model, 'random_forest_model.pkl')
print("Model saved as 'random_forest_model.pkl'")

# Optional: Verify loading the model
loaded_model = joblib.load('random_forest_model.pkl')
sample_input = [X.iloc[0].tolist()]  # Replace with any sample input from your dataset
sample_prediction = loaded_model.predict(sample_input)
print(f"Sample Input: {sample_input}")
print(f"Sample Prediction: {sample_prediction}")
