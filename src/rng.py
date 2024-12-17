import random

def generate_patient_scenario():
    # For demonstration, return a fixed scenario
    # Later, implement the actual probabilistic model described earlier.
    scenario = {
        "gender": "Male",
        "age": 62,
        "race": "White",
        "occupation": "Shipyard worker",
        "smoking_history": "Ex-smoker",
        "symptom_severity": "Moderate dyspnea, persistent cough for 1 year",
        "additional_clue": "No systemic symptoms",
        "diagnosis": "Asbestosis"  # The 'answer key'
    }
    return scenario