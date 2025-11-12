=import json
import boto3

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        text = body.get("text", "")

        if not text:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"error": "No text provided"})
            }

        comprehend = boto3.client("comprehend")
        response = comprehend.detect_sentiment(Text=text, LanguageCode="en")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({
                "Sentiment": response["Sentiment"],
                "SentimentScore": response["SentimentScore"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
