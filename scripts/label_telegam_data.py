import pandas as pd

# Load the dataset
file_path = 'telegram_data.csv'  # Replace with your dataset file path
data = pd.read_csv(file_path)

# Extract the "Message Text" column and drop missing values
messages = data["Message Text"].dropna().tolist()

# Define a function to tokenize and label entities in the message text
def label_message(message):
    tokens = message.split()  # Tokenize by spaces
    labeled_tokens = []
    
    for token in tokens:
        if "ዋጋ" in token:  # Start of a price entity
            labeled_tokens.append(f"{token} B-PRICE")
        elif "ብር" in token:  # Inside a price entity
            labeled_tokens.append(f"{token} I-PRICE")
        elif any(loc in token for loc in ["ደፋር", "ጊዮርጊስ"]):  # Location entities
            labeled_tokens.append(f"{token} B-LOC")
        elif any(prod in token for prod in ["እስቲመር", "ጸጉር", "ጡጦ", "ማዘዝ"]):  # Product entities
            labeled_tokens.append(f"{token} B-PRODUCT")
        else:  # Outside any entity
            labeled_tokens.append(f"{token} O")
    
    labeled_tokens.append("")  # Blank line to separate sentences/messages
    return labeled_tokens

# Label a subset of the dataset (30 messages)
subset_size = 30
subset = messages[:subset_size]

# Process each message in the subset
labeled_data = []
for message in subset:
    labeled_data.extend(label_message(message))

# Save the labeled data in CoNLL format
output_file_path = 'labeled_telegram_subset.conll'
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(labeled_data))

print(f"Labeled data saved to {output_file_path}")
