import gradio as gr
from .rng import generate_patient_scenario
from .llm import generate_case_study_from_scenario
from .logic import GameState

game_state = GameState()

def start_day():
    # Start a day, generate first patient
    scenario = generate_patient_scenario()
    case_study = generate_case_study_from_scenario(scenario)
    game_state.next_patient(scenario, case_study)
    return (f"Patient Profile:\n{case_study['patient_profile']}\n\n"
            f"Clinical Scenario:\n{case_study['clinical_scenario']}\n\n"
            f"Would you like to order CXR or HRCT next? "
            f"(CXR left: {game_state.max_cxr}, HRCT left: {game_state.max_hrct})",
            "")

def order_cxr():
    if game_state.max_cxr > 0:
        game_state.max_cxr -= 1
        return f"CXR Findings:\n{game_state.current_case['cxr_findings']}", ""
    else:
        return "No CXR left for today!", ""

def order_hrct():
    if game_state.max_hrct > 0:
        game_state.max_hrct -= 1
        return f"HRCT Findings:\n{game_state.current_case['hrct_findings']}", ""
    else:
        return "No HRCT left for today!", ""

def show_options():
    # Show multiple choice
    options_text = "Select the best diagnosis & treatment option:\n"
    for choice in game_state.current_case["choices"]:
        options_text += f"{choice['option']}: {choice['text']}\n"
    return options_text

def submit_answer(answer):
    correct = game_state.submit_answer(answer)
    # Find the chosen option explanation
    chosen_explanation = ""
    for c in game_state.current_case["choices"]:
        if c["option"] == answer:
            chosen_explanation = c["explanation"]
            break
    return f"Your choice: {answer}\n\n{chosen_explanation}\n\nCorrect answer was: {correct}"

with gr.Blocks() as demo:
    gr.Markdown("# ILD Diagnostic Training Game")
    start_btn = gr.Button("Start Day")
    cxr_btn = gr.Button("Order CXR", visible=False)
    hrct_btn = gr.Button("Order HRCT", visible=False)
    show_options_btn = gr.Button("Show Options", visible=False)
    answer_input = gr.Textbox(label="Enter A, B, C, or D", visible=False)
    submit_answer_btn = gr.Button("Submit Answer", visible=False)

    scenario_output = gr.Textbox(label="Scenario", interactive=False)
    imaging_output = gr.Textbox(label="Imaging Results", interactive=False)

    def handle_start():
        scenario_txt, imaging_txt = start_day()
        return scenario_txt, imaging_txt, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

    start_btn.click(handle_start, outputs=[scenario_output, imaging_output, cxr_btn, hrct_btn, show_options_btn, answer_input])

    cxr_btn.click(order_cxr, outputs=[imaging_output, scenario_output])
    hrct_btn.click(order_hrct, outputs=[imaging_output, scenario_output])

    def handle_show_options():
        return show_options(), gr.update(visible=True)

    show_options_btn.click(handle_show_options, outputs=[scenario_output, submit_answer_btn])

    submit_answer_btn.click(submit_answer, inputs=answer_input, outputs=scenario_output)


app = demo