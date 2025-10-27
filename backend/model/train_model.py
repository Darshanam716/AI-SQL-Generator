from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
import os

# Model & tokenizer
MODEL_NAME = "t5-small"  # You can also use "t5-base" if your GPU has enough memory
MODEL_DIR = "./model/t5_sql_model"

# Load tokenizer & model
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# Load WikiSQL dataset
# We only use a small portion for demo; remove 'select' for full dataset
dataset = load_dataset("wikisql", split="train[:1%]")  

# Preprocess the dataset
def preprocess(example):
    input_text = "translate English to SQL: " + example["question"]
    target_text = example["sql"]["human_readable"]
    input_ids = tokenizer.encode(input_text, truncation=True, padding="max_length", max_length=128)
    target_ids = tokenizer.encode(target_text, truncation=True, padding="max_length", max_length=128)
    return {"input_ids": input_ids, "labels": target_ids}

tokenized_dataset = dataset.map(preprocess)

# Set training args
training_args = TrainingArguments(
    output_dir=MODEL_DIR,
    num_train_epochs=1,
    per_device_train_batch_size=2,
    save_steps=1000,
    save_total_limit=1,
    logging_steps=100,
    learning_rate=5e-5,
    weight_decay=0.01,
    remove_unused_columns=False,
    report_to="none",
)

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Train
trainer.train()

# Save model & tokenizer locally
os.makedirs(MODEL_DIR, exist_ok=True)
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)

print(f"Model trained and saved at: {MODEL_DIR}")
