#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:04:17 2024

@author: colin
"""

import os
from os.path import join as pjoin
from os.path import exists as pexists
import sys
import subprocess
import shutil
import argparse
import time


def bids_flairstar(bids, sub, ses, flair_ref, t2star_ref, deriv='flairstar', out_name=None):
    
    print('flairstar pipeline only works with docker')
    print('Please use_docker option')
        
  
def bids_flairstar_docker(bids, sub, ses, flair_ref, t2star_ref, deriv='flairstar', out_name=None):
    
    print('flairstar')
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
    
    os.makedirs(sub_ses_deriv, exist_ok=True)
    
    flair_p, flair_in = rename_path_sub_ses(bids, sub, ses, flair_ref)
    t2star_p, t2star_in = rename_path_sub_ses(bids, sub, ses, t2star_ref)
    
    if not out_name:
        
        out_name = f'sub-{sub}_ses-{ses}_FLAIRstar.nii.gz'
        
    subprocess.Popen(f"docker run --rm -v {flair_p}:/data/flair -v {t2star_p}:/data/t2star -v {sub_ses_deriv}:/data/deriv blakedewey/flairstar -f {pjoin('/data/flair', flair_in)} -t {pjoin('/data/t2star', t2star_in)} -o {pjoin('/data/deriv', f'{out_name}.nii.gz')}", shell=True).wait()
    
    print('docker has finished')

    
def rename_path_sub_ses(bids, sub, ses, path):
    """


    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    sub : TYPE
        DESCRIPTION.
    ses : TYPE
        DESCRIPTION.

    Returns
    -------
    path_name : TYPE
        DESCRIPTION.

    """

    if not is_subpath(path, bids):
        print('[ERROR] path selected not in the BIDS directory')
        return
    
    rel_path = os.path.relpath(path, bids).split(os.sep)
    file = rel_path[-1]
    new_path = []
    for p in rel_path[:-1]:
        if 'sub-' in p:
            new_path.append(f'sub-{sub}')
        elif 'ses-' in p:
            new_path.append(f'ses-{ses}')
        else:
            new_path.append(p)
    new_file = []
    for k in file.split('_'):
        if 'sub-' in k:
            new_file.append(f'sub-{sub}')
        elif'ses-' in k:
            new_file.append(f'ses-{ses}')
        else:
            new_file.append(k)
    return pjoin(bids, *new_path), '_'.join(new_file)
    

def is_subpath(main_path, sub_path):
    main_path = os.path.abspath(main_path)
    sub_path = os.path.abspath(sub_path)
    try:
        common_path = os.path.commonpath([main_path, sub_path])
        return common_path == sub_path
    except ValueError:
        return False


def get_session_list(bids, subj, ses_details, check_if_exist=True):
    """Helper function to get the list of sessions for a given subject."""
    sess = []
    if ses_details == 'all':
        for d in os.listdir(pjoin(bids, f'sub-{subj}')):
            if d.startswith('ses-'):
                sess.append(d.split('-')[1])
    else:
        for s in ses_details.split(','):
            if '-' in s:
                s0, s1 = map(int, s.split('-'))
                for si in range(s0, s1 + 1):
                    si_str = str(si).zfill(2)
                    if check_if_exist:
                        if os.path.isdir(pjoin(bids, f'sub-{subj}', f'ses-{si_str}')):
                            sess.append(si_str)
                    else:
                        sess.append(si_str)
            else:
                if check_if_exist:
                    if os.path.isdir(pjoin(bids, f'sub-{subj}', f'ses-{s}')):
                        sess.append(s)
                else:
                    sess.append(s)
    return sess

def process_subject_range(bids, sub_range, ses_details, check_if_exist=True):
    """Helper function to process a range of subjects."""
    subjects_and_sessions = []
    sub0, sub1 = map(int, sub_range.split('-'))
    for subi in range(sub0, sub1 + 1):
        subi_str = str(subi).zfill(3)
        if not os.path.isdir(pjoin(bids, f'sub-{subi_str}')) and check_if_exist:
            continue
        sess = get_session_list(bids, subi_str, ses_details, check_if_exist=check_if_exist)
        subjects_and_sessions.append((subi_str, sess))
    return subjects_and_sessions

def find_subjects_and_sessions(bids, sub, ses, check_if_exist=True):
    subjects_and_sessions = []

    if sub == 'all':
        # Process all subjects
        for dirs in os.listdir(bids):
            if dirs.startswith('sub-'):
                subj = dirs.split('-')[1]
                sess = get_session_list(bids, subj, ses)
                subjects_and_sessions.append((subj, sess))
    else:
        # Process specified subjects
        for sub_item in sub.split(','):
            if '-' in sub_item:
                subjects_and_sessions.extend(process_subject_range(bids, sub_item, ses, check_if_exist=check_if_exist))
            else:
                if not os.path.isdir(pjoin(bids, f'sub-{sub_item}')) and check_if_exist:
                    continue
                sess = get_session_list(bids, sub_item, ses, check_if_exist=check_if_exist)
                subjects_and_sessions.append((sub_item, sess))
    
    return sorted(subjects_and_sessions)
    


if __name__ == '__main__':
    
    description = '''
bids_flairstar:
    Compute flairstar image based on the docker blakedewey/flairstar
    '''
    
    usage = '\npython %(prog)s bids sub ses [OPTIONS]'
    
    parser = argparse.ArgumentParser(description=description, usage=usage)
    
    parser.add_argument('bids', type=str, help='path towards a bids formatted database')
    parser.add_argument('sub', type=str, help='sub ID or list of sub ID to process (e.g. 001,002). The keyword "all" will select all subjects of the database, while "-" allow to select subject ID in between two border (e.g. 001-010)')
    parser.add_argument('ses', type=str, help='ses ID or list of ses ID to process (e.g. 01,02). The keyword "all" will select all sessions of the database, while "-" allow to select session ID in between two border (e.g. 01-10)')
    parser.add_argument('--flair-path', '-f', dest='flair_path', type=str, help='reference path of input flair image', required=True)
    parser.add_argument('--t2star-path', '-t2', dest='t2star_path', type=str, help='reference path of input magnitude T2starw image', required=True)
    parser.add_argument('--derivative', '-d', dest='deriv', type=str, help='derivative folder name to store the output (default: flairstar)', default='flairstar', required=False)
    parser.add_argument('--out-name', '-o', dest='out_name', type=str, help='name of the output sequence name (default: FLAIRstar)', default=None, required=False)
    parser.add_argument('--use-docker', dest='use_docker', help='use docker version of flairstar (blakedewey/flairstar) instead of local one (default=True)', action='store_const', const=False, default=True, required=False)
    
    # Parse the arguments
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # This block catches the SystemExit exception raised by argparse when required args are missing
        if e.code != 0:  # Non-zero code indicates an error
            parser.print_help()
        sys.exit(e.code)
        
    bids = args.bids
    
    subjects_and_sessions = find_subjects_and_sessions(bids, args.sub, args.ses)
    
    for sub, sess in subjects_and_sessions:
        for ses in sess:
            print(sub, ses)
            
            if args.use_docker:
                bids_flairstar_docker(bids, sub, ses, args.flair_path, args.t2star_path, deriv=args.deriv, out_name=args.out_name)
            else:
                bids_flairstar(bids, sub, ses, args.flair_path, args.t2star_path, deriv=args.deriv, out_name=args.out_name)
    
    