import html
import logging

import click
import feedparser
import pandas as pd

NEWS_FEED_URL = "https://www.cnbc.com/id/19746125/device/rss/rss.xml"
COLUMNS_TO_SAVE = ["id", "published", "title", "summary"]

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--data_path", help="Path to the input data CSV file")
def data_load(data_path: str) -> None:
    """
    Fetches financial news from the specified RSS feed URL, processes the data, and saves it to a CSV file.

    Parameters:
        data_path (str): The path where the processed data will be saved as a CSV file.
    """
    logging.info("Fetching financial news from the RSS feed...")
    news_feed = feedparser.parse(NEWS_FEED_URL)
    logging.info("News fetched successfully.")

    df = pd.DataFrame(news_feed.entries)[COLUMNS_TO_SAVE]
    df["published"] = pd.to_datetime(df["published"])
    df["title"] = df["title"].map(html.unescape)
    df["summary"] = df["summary"].map(html.unescape)

    logging.info(f"Saving the processed data to '{data_path}'...")
    df.to_csv(data_path, sep="\t", index=False)
    logging.info("Data saved successfully.")


if __name__ == "__main__":
    data_load()
