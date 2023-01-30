#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    
    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Start cleaning: Removing outliers")
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    logger.info("Converting 'last_review' column to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info(f"Saving output dataframe as '{args.output_artifact}'")
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
 )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Raw data that will be cleaned",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Name of output file",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Output type for the output file",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Description of output file",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help="Min price, so we can cap and remove the ouliers",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help="Max price, so we can cap and remove the ouliers",## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
