#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="exercise_5", job_type="process_data")

    ## YOUR CODE HERE
    #== artifact processing message ==
    logger.info("Fetching input artifact")

    #== load in the artifact ==
    artifact = (
        run
        .use_artifact(args.input_artifact)
    )

    #== assign artifact to local variable ==
    artifact_path = (
        artifact.file()
    )

    #== artifact processing message ==
    logger.info("Reading in the artifact")

    #== read in the artifact ==
    df = (
        pd
        .read_parquet(
            artifact_path
        )
    )

    #== artifact processing message ==
    logger.info("Preprocessing the artifact")

    #== drop duplicates ==
    df = (
        df
        .drop_duplicates()
        .reset_index(
            drop = True
        )
    )

    #== artifact processing message ==
    logger.info("Fill NaNs and concatenate")

    #== fill NaNs & concatenate ==
    df = (
        df
        .assign(
            title = df["title"]
                    .fillna(
                        value = ""
                    ),
            song_name = df["song_name"]
                        .fillna(
                            value = ""
                        ),
            text_feature = lambda col: col["title"] + " " + col["song_name"]
        )
    )

    #== artifact processing message ==
    logger.info("Save the artifact locally and log it to W&B")

    #== assign output file ==
    outfile = f"{args.artifact_name}"

    #== save locally ==
    df.to_csv(
        outfile,
        index = False
    )

    #== artifact processing message ==
    logger.info("Build the artifact and attach the file")

    #== build artifact ==
    artifact = (
        wandb.Artifact(
            name = args.artifact_name,
            type = args.artifact_type,
            description = args.artifact_description
        )
    )


    #== attach file to artifact ==
    artifact.add_file(
        outfile
    )

    #== artifact processing message ==
    logger.info("Log the artifact to W&B")

    #== log artifact to W&B ==
    run.log_artifact(
        artifact
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
