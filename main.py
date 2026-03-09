import boto3
import json

# Initialize the Bedrock Runtime client
client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_virtual_scientist_response(user_query):
    # This structure targets the Amazon Nova Pro model
    payload = {
        "inferenceConfig": {"temperature": 0.1},
        "messages": [
            {
                "role": "user",
                "content": [{"text": user_query}]
            }
        ]
    }

    response = client.invoke_model(
        modelId="amazon.nova-pro-v1:0",
        body=json.dumps(payload)
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['output']['message']['content'][0]['text']

# Example Usage:
# print(get_virtual_scientist_response("How can I make a battery at home using lemons?"))
