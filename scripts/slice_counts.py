# this script finds the count indices for sm2 

import pandas as pd
import numpy as np
import torch 

import gc
import argparse
import os

def get_idx_dict(metadata):
    """
    Gets index of each region label in metadata
    """

    idx_dict = {}
    for x in metadata.region_label.unique():
        idx_dict[x] = np.where(metadata.region_label == x)[0]

    return idx_dict

def write_all_regions(metadata_fpath, counts_fpath, wpath):
    """
    Saves each subset of the cou
    """
    meta = pd.read_csv(metadata_fpath, index_col=0, low_memory=False)
    counts = torch.from_numpy(np.load(counts_fpath))

    index_dict = get_idx_dict(meta)

    for x in index_dict:
        torch.save(counts[index_dict[x], :], os.path.join(wpath, x + ".pt"))
        gc.collect()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data", type=str, choices=["sm2","tenx"],
        help="select dataset to slice into regions")

    args = parser.parse_args()

    if args.data == "sm2":
        dpath =  "/bigstore/binfo/mouse/Brain/Sequencing/Allen_SmartSeq_2020/"
        metadata_fpath = os.path.join(dpath, "metadata.csv")
        counts_fpath = os.path.join(dpath, "counts.npy")
        wpath = "/bigstore/GeneralStorage/jperrie/probe_design/data/sm2/"
    elif args.data == "tenx":
        dpath =  "/bigstore/binfo/mouse/Brain/Sequencing/Allen_10X_2020/"
        metadata_fpath = os.path.join(dpath, "metadata.csv")
        counts_fpath = os.path.join(dpath, "counts.npy")
        wpath = "/bigstore/GeneralStorage/jperrie/probe_design/data/tenx/"

    write_all_regions(metadata_fpath, counts_fpath, wpath)