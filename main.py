import os
from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Prepare the lore text from the assets
def prep_assets():
    all_text = ''
    for filename in os.listdir('assets'):
        if filename.endswith('.txt'):
            with open(os.path.join('assets', filename), 'r') as file:
                all_text += file.read() + '\n'
    return all_text

# Function to process the user input and generate model output
def on_button_action(state):
    state.output += '\n' + state.user_input
    input_ids = state.tokenizer(state.output, return_tensors="pt")["input_ids"].to(state.device)
    #combined_input_ids = torch.cat((state.world_lore_ids, input_ids), dim=-1)
    #output_ids = state.model.generate(combined_input_ids, max_length=60, num_beams=7, do_sample=False)
    output_ids = state.model.generate(input_ids, max_length=20, num_beams=5, do_sample=False)
    state.output += '\n' + state.tokenizer.decode(output_ids[0], skip_special_tokens=True)

def on_change(state, var_name, var_value):
    #print(f"{var_name} | {var_value} \n")
    return

if __name__ == "__main__":

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    
    world_lore = prep_assets()
    world_lore_ids = tokenizer(world_lore, return_tensors="pt")["input_ids"].to(device) #we encode world lore to use as context for queries
    
    user_input = ""
    output = "You are standing in an open field west of a white house, with a boarded front door."

    # Define the page layout
    with tgb.Page() as page:
        tgb.text("# Text-based RPG", mode="md")
        tgb.text("{output}")
        tgb.input("{user_input}")
        tgb.button("Do!", on_action=on_button_action)

    # Run the GUI with state variables
    Gui(page).run(
        debug=True,
        world_lore_ids=world_lore_ids,
        model=model,
        tokenizer=tokenizer,
        device=device,
        user_input=user_input,
        output=output
    )
