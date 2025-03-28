from transformers import pipeline

# Load the model (make sure it supports text generation)
model_name = "gpt2"  # Example: Replace with your Hugging Face model
gen_pipeline = pipeline("text-generation", model=model_name)

# Example YAML input
yaml_input = """
source:
  type: "Kafka"
  topic: "events"
  parallelism: 20

transform:
  type: "SQL"
  query: "SELECT * FROM events"
  state_backend: "rocksdb"

sink:
  type: "S3"
  bucket: "flink-output"
"""

# Construct a validation prompt
prompt = f"""
You are an expert in Apache Flink real-time data processing.

Given the following YAML configuration:
---
{yaml_input}
---

Validate it based on these rules:
1. Parallelism should be ≤ 5 for small-scale jobs.
2. Checkpointing must be defined.
3. Ensure all required fields are present.
4. Suggest performance improvements.

Return a JSON response with:
- "errors": List of detected issues.
- "suggested_fixes": How to fix them.
- "corrected_yaml": A properly formatted YAML with fixes applied.
"""

# Generate response
response = gen_pipeline(prompt, max_length=500)

# Print the output
print(response[0]['generated_text'])