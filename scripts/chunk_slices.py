# this script batches counts data 

import pandas as pd
import numpy as np
import torch

import gc 
import argparse 
import os

from collections import Counter

def load_counts(filepaths):
    """
    Load counts from multiple files and concat
    """
    counts = torch.load(filepaths[0])
    
    for i in range(1, len(filepaths)):
        counts = torch.cat((counts, torch.load(filepaths[i])), 0)
        gc.collect()

    return counts

def get_metadata(region_labels, mpath, rpath):
    """
    Get metadata for regions and verify that they match metadata. 
    The sm2 and tenx exclusive labels should not be mixed
    """
    meta = pd.read_csv(mpath, index_col=0, low_memory=False)
    uniq_region_labels = meta.region_label.unique()
    fpaths = []

    # raise error if mismatch
    for x in region_labels:
        if x not in uniq_region_labels:
            ValueError("regions provided do not match data source")
        fpaths += [os.path.join(rpath, x + ".pt")]

    logical_index = np.array([(meta.region_label == x) for x in region_labels])

    lor = logical_index[0]

    for i in range(1, len(logical_index)):
        lor = np.logical_or(lor, logical_index[i])

    return meta.loc[lor], fpaths

def generate_batches(fpaths, meta, wpath, clvl="Level_3_subclass_label", flvl="Level_4_supertype_label", batch_size=50, min_labels=10, nreps=10):
    """
    Generate batches from count data and write to file

    Input
    -----
    fpaths: paths of each region
    meta: metadata of regions
    wpath: path to write batches to
    clvl: coarse level of labels to be used (field from metadata)
    flvl: fine level of labels to be used (field from metadata)
    batch_size: size of downsampled classes
    min_labels: minimum size of class to be considered
    nreps: number of batches to be created
    """
    counts = load_counts(fpaths)
    labels = meta[clvl]
    lab_count = Counter(labels)
    lab_count_thr = {x : np.where(labels==x)[0] for x in lab_count if lab_count[x] > min_labels}

    for i in range(nreps):
        batch_index = np.concatenate([np.random.choice(lab_count_thr[x], size=batch_size) for x in lab_count_thr])
        clab = meta.iloc[batch_index][clvl].values
        flab = meta.iloc[batch_index][flvl].values
        batch_counts = counts[batch_index, :]

        data = {}
        data["index"] = batch_index
        data["clab"] = clab
        data["flab"] = flab
        data["counts"] = batch_counts

        torch.save(data, os.path.join(wpath, str(i) + ".pt"))
        gc.collect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--region", type=str, nargs="+",
        choices = ["ACA", "AUD", "ENTl", "GU", "MOp", "ORB", "PL-ILA", "RSP", "SSs", "TEa-PERI-ECT", "VIS",
            "AI", "CLA", "ENTm", "HIP", "MOs-FRP", "PAR-POST-PRE", "PTLp", "SSp", "SUB-ProS", "VISp",
            "PL;ILA;ORB.pt", "VISam;VISpm.pt", "AId;AIv;AIp.pt", "ENT", "MOs;FRP.pt", "SSs;GU;VISC;AIp.pt",
            "VIS1", "AId;AIv.pt", "PAR;POST;PRE;SUB;ProS.pt", "TEa;PERI;ECT.pt"],
        help="select regions to analyze")

    parser.add_argument("-r", "--read", type=str,
        help="directory to read regions from")

    parser.add_argument("-w", "--write", type=str,
        help="directory to write batches to")

    parser.add_argument("-d", "--data", type=str, choices=["sm2","tenx"],
        help="select dataset to slice into regions")

    args = parser.parse_args()

    if args.data == "sm2":
        dpath =  "/bigstore/binfo/mouse/Brain/Sequencing/Allen_SmartSeq_2020/"
        metadata_fpath = os.path.join(dpath, "metadata.csv")
    elif args.data == "tenx":
        dpath =  "/bigstore/binfo/mouse/Brain/Sequencing/Allen_10X_2020/"
        metadata_fpath = os.path.join(dpath, "metadata.csv")

    meta, fpaths = get_metadata(args.region, metadata_fpath, args.read)
    generate_batches(fpaths, meta, args.write)
    

