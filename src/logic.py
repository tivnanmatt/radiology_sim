class GameState:
    def __init__(self, daily_patients=10, max_cxr=8, max_hrct=5):
        self.daily_patients = daily_patients
        self.max_cxr = max_cxr
        self.max_hrct = max_hrct
        self.current_patient_index = 0
        self.score = 0
        self.current_case = None

    def next_patient(self, scenario, case_study):
        self.current_case = case_study
        self.current_patient_index += 1
        self.max_cxr = 8  # reset per patient if desired
        self.max_hrct = 5

    def submit_answer(self, answer):
        # Find answer in choices
        correct_option = "B"  # from the mock scenario
        if answer == correct_option:
            self.score += 1
        return correct_option