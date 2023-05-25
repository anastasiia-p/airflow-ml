import json
from collections import defaultdict
from datetime import datetime, timedelta

NEWS_MAX_LAG = timedelta(days=1)
news_by_labels = defaultdict(list)


def aggregate_predictions(pred_data_path: str, result_data_path: str) -> None:
    """
    Aggregate predictions from the input JSON file by labels and filter by date.

    Args:
        pred_data_path (str): Path to the input JSON file containing predictions.
        result_data_path (str): Path to save the aggregated results as a JSON file.
    """
    with open(pred_data_path, "r") as f:
        news = json.load(f)

    for item in news.values():
        news_datetime = datetime.strptime(item["published"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - news_datetime < NEWS_MAX_LAG:
            news_by_labels[item["label"]].append(item["summary"])

    with open(result_data_path, "w") as f:
        json.dump(news_by_labels, f)
