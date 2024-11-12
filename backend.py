# app.py (Flask backend)
from flask import Flask, request, jsonify
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Load lore text
def load_lore():
    lore = ""
    for filename in os.listdir('assets'):
        if filename.endswith('.txt'):
            with open(os.path.join('assets', filename), 'r') as f:
                lore += f.read() + "\n"
    return lore

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    user_input = data.get("input", "")
    
    # Process input with world lore
    input_text = world_lore + user_input
    input_ids = tokenizer(input_text, return_tensors="pt")["input_ids"].to(device)
    #combined_input_ids = torch.cat((world_lore_ids, input_ids), dim=-1)
    #output_ids = model.generate(combined_input_ids, max_length=60, num_beams=7, do_sample=False)
    output_ids = model.generate(input_ids, max_length=60, num_beams=5, do_sample=False)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return jsonify({"response": output_text})

if __name__ == "__main__":
    # Initialize model and tokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #model_name = "gpt2"
    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

    world_lore = load_lore()
    world_lore_ids = tokenizer(world_lore, return_tensors="pt")["input_ids"].to(device)

    app.run(port=5000)
