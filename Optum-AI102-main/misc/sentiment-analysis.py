from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        reviews_folder = 'reviews'
        
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            file_path = os.path.join(reviews_folder, file_name)
            with open(file_path, encoding='utf8') as file:
                text = file.read()
            
            print('\n-------------\n' + file_name)
            print('\n' + text)

            sentiment_analysis = ai_client.analyze_sentiment(documents=[text])[0]

            print("\nSentence Sentiments:")
            for sentence in sentiment_analysis.sentences:
                print("\t\"{}\" - {} (positive={:.2f}, neutral={:.2f}, negative={:.2f})".format(
                    sentence.text,
                    sentence.sentiment,
                    sentence.confidence_scores.positive,
                    sentence.confidence_scores.neutral,
                    sentence.confidence_scores.negative))

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
