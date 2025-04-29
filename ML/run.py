import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# 1. Data Collection - Simulated Data
np.random.seed(42)

# Simulate User and Event IDs
user_ids = np.arange(1, 101)  # 100 users
event_ids = np.arange(1, 51)  # 50 events

# Create a DataFrame for user-event interactions (Random interaction for simulation)
data = []
for user in user_ids:
    num_interactions = np.random.randint(1, 6)  # Each user interacts with 1-5 events
    interacted_events = np.random.choice(event_ids, num_interactions, replace=False)
    for event in interacted_events:
        data.append([user, event, 1])  # 1 means user interacted with the event
    # Simulate non-interacted events
    non_interacted_events = np.setdiff1d(event_ids, interacted_events)
    for event in non_interacted_events:
        data.append([user, event, 0])  # 0 means user did not interact with the event

# Convert to DataFrame
interaction_df = pd.DataFrame(data, columns=["User_ID", "Event_ID", "Interacted"])

# Simulate Event Metadata (for feature creation)
event_metadata = {
    'Event_ID': event_ids,
    'Event_Type': np.random.choice(['Conference', 'Concert', 'Festival'], 50),
    'Event_Genre': np.random.choice(['Tech', 'Music', 'Sports'], 50),
    'Location': np.random.choice(['NYC', 'LA', 'SF', 'Chicago', 'Miami'], 50)
}
event_df = pd.DataFrame(event_metadata)

# 2. Data Preprocessing - Feature Engineering
# Encode categorical features
le_event_type = LabelEncoder()
le_event_genre = LabelEncoder()
le_location = LabelEncoder()

event_df['Event_Type'] = le_event_type.fit_transform(event_df['Event_Type'])
event_df['Event_Genre'] = le_event_genre.fit_transform(event_df['Event_Genre'])
event_df['Location'] = le_location.fit_transform(event_df['Location'])

# Merge event data with user interaction data
interaction_df = interaction_df.merge(event_df, on="Event_ID", how="left")

# 3. Model Training: Random Forest Classifier
# Features: User_ID, Event_ID, Event_Type, Event_Genre, Location
# Label: Interacted (1 if interacted, 0 if not)

X = interaction_df[['User_ID', 'Event_ID', 'Event_Type', 'Event_Genre', 'Location']]
y = interaction_df['Interacted']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 4. Model Evaluation: Accuracy & Classification Report
y_pred = rf_model.predict(X_test)

# Evaluate model
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 5. Predicting User Preferences for New Events

def predict_user_interaction(user_id, event_id, model, event_df):
    """
    Predict if a user will interact with a given event using the trained model.
    """
    # Retrieve the event details for encoding
    event_details = event_df[event_df['Event_ID'] == event_id]
    if event_details.empty:
        return f"Event ID {event_id} not found."
    
    # Prepare the feature vector for prediction
    event_details = event_details[['Event_ID', 'Event_Type', 'Event_Genre', 'Location']]
    event_details['User_ID'] = user_id
    
    # Encode categorical features for prediction
    event_details['Event_Type'] = le_event_type.transform(event_details['Event_Type'])
    event_details['Event_Genre'] = le_event_genre.transform(event_details['Event_Genre'])
    event_details['Location'] = le_location.transform(event_details['Location'])

    # Predict if the user will interact with this event
    prediction = model.predict(event_details[['User_ID', 'Event_ID', 'Event_Type', 'Event_Genre', 'Location']])
    
    return "User will interact with the event" if prediction[0] == 1 else "User will not interact with the event"

# Example: Predict if User 1 will interact with Event 3
user_id = 1
event_id = 3
prediction = predict_user_interaction(user_id, event_id, rf_model, event_df)
print(f"\nPrediction for User {user_id} and Event {event_id}: {prediction}")
