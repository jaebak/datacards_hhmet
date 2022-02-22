#!/bin/env python
import os
import sys
import multiprocessing
import glob
import subprocess
from time import time
import argparse

def getTChiHHMassPoints():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  mass_points = []
  with open(script_dir+"/txt/higgsino2DFileNames.txt", 'r') as namesFile:
    for line in namesFile:
      x = line.split('_')
      hino_mass = int(x[5])
      LSP_mass = int(x[6])
      if hino_mass>810: break;
      mass_points.append([hino_mass, LSP_mass])
    #Add 1D scan
    for i in range(0, 27):
      hino_mass=150+i*25
      mass_points.append([hino_mass, 1])
  return mass_points

def getT5HHMassPoints():
  return 


def runCommandForMultiProcessing(command):
  print(command)
  process = subprocess.Popen(command[1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = process.communicate()
  return out.decode("utf-8")+'\n'+err.decode("utf-8")

def runCommands(commands):
  commands_info = [(index, commands[index]) for index in range(len(commands))]
  pool = multiprocessing.Pool()
  pool.map(runCommandForMultiProcessing, commands_info)

def makeMergeHiggsinoCommands(whichDString,signal,hino,LSP,dataMCString, phase_space):
  hino = int(hino)
  LSP = int(LSP)
  resLSP = LSP;
  if (resLSP==1): resLSP=0;
  if (resLSP%5!=0): resLSP=resLSP+2;
  combineCommands = []
  # Make combine commands
  # Boosted only
  if 'boosted' in phase_space:
    combineCommands.append("combineCards.py SRMerge_%s%s%d_LSP%d_%s.txt CRBMerge_%s%s%d_LSP%d_%s.txt CRCMerge_%s%s%d_LSP%d_%s.txt CRDMerge_%s%s%d_LSP%d_%s.txt CREMerge_%s%s%d_LSP%d_%s.txt > %s%s%d_LSP%d_BothBoostedH_%s.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
  #Resolved only
  if 'resolved' in phase_space:
    combineCommands.append("combineCards.py resData/%sTChiHH_%s/datacard-%s_mChi-%d_mLSP-%d_Tune_2016,2017,2018_priority1_resolved.txt > %s%s%d_LSP%d_%s_ResOnly.txt "%(whichDString,dataMCString,signal,hino,resLSP,whichDString,signal,hino,LSP,dataMCString))
  #BoostedOnlyVeto
  if 'combined' in phase_space:
    combineCommands.append("combineCards.py SRMerge_%s%s%d_LSP%d_%s_veto.txt CRBMerge_%s%s%d_LSP%d_%s_veto.txt CRCMerge_%s%s%d_LSP%d_%s_veto.txt CRDMerge_%s%s%d_LSP%d_%s_veto.txt CREMerge_%s%s%d_LSP%d_%s_veto.txt > %s%s%d_LSP%d_BothBoostedH_%s_veto.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
    combineCommands.append("combineCards.py %s%s%d_LSP%d_BothBoostedH_%s_veto.txt resData/%sTChiHH_%s/datacard-%s_mChi-%d_mLSP-%d_Tune_2016,2017,2018_priority1_resolved.txt > %s%s%d_LSP%d_%s_Combo.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,dataMCString,signal,hino,resLSP,whichDString,signal,hino,LSP,dataMCString))
  return combineCommands

def makeMergeGluinoCommands(whichDString,signal,hino,LSP,dataMCString, phase_space):
  hino = int(hino)
  LSP = int(LSP)
  resLSP = LSP;
  if (resLSP==1): resLSP=0;
  if (resLSP%5!=0): resLSP=resLSP+2;
  combineCommands = []
  # Make combine commands
  # Boosted only
  if 'boosted' in phase_space:
    combineCommands.append("combineCards.py SRMerge_%s%s%d_LSP%d_%s.txt CRBMerge_%s%s%d_LSP%d_%s.txt CRCMerge_%s%s%d_LSP%d_%s.txt CRDMerge_%s%s%d_LSP%d_%s.txt CREMerge_%s%s%d_LSP%d_%s.txt > %s%s%d_LSP%d_BothBoostedH_%s.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
  #Resolved only
  if 'resolved' in phase_space:
    combineCommands.append("combineCards.py resData/%sT5HH_%s/datacard-%s_mGluino-%d_mLSP-%d_Tune_2016,2017,2018_priority1_resolved.txt > %s%s%d_LSP%d_%s_ResOnly.txt "%(whichDString,dataMCString,signal,hino,resLSP,whichDString,signal,hino,LSP,dataMCString))
  #BoostedOnlyVeto
  if 'combined' in phase_space:
    combineCommands.append("combineCards.py SRMerge_%s%s%d_LSP%d_%s_veto.txt CRBMerge_%s%s%d_LSP%d_%s_veto.txt CRCMerge_%s%s%d_LSP%d_%s_veto.txt CRDMerge_%s%s%d_LSP%d_%s_veto.txt CREMerge_%s%s%d_LSP%d_%s_veto.txt > %s%s%d_LSP%d_BothBoostedH_%s_veto.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
    combineCommands.append("combineCards.py %s%s%d_LSP%d_BothBoostedH_%s_veto.txt resData/%sT5HH_%s/datacard-%s_mGluino-%d_mLSP-%d_Tune_2016,2017,2018_priority1_resolved.txt > %s%s%d_LSP%d_%s_Combo.txt "%(whichDString,signal,hino,LSP,dataMCString,whichDString,dataMCString,signal,hino,resLSP,whichDString,signal,hino,LSP,dataMCString))
  return combineCommands

def makeCombineCommands(whichDString,signal,hino,LSP,dataMCString, phase_space):
  hino = int(hino)
  LSP = int(LSP)
  resLSP = LSP;
  if (resLSP==1): resLSP=0;
  if (resLSP%5!=0): resLSP=resLSP+2;
  combineCommands = []
  # Make combine commands
  # Boosted only
  if 'boosted' in phase_space:
    combineCommands.append("combine -M AsymptoticLimits -n %s%s%d_LSP%d_BothBoostedH_%s %s%s%d_LSP%d_BothBoostedH_%s.txt " %(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
  #Resolved only
  if 'resolved' in phase_space:
    combineCommands.append("combine -M AsymptoticLimits -n %s%s%d_LSP%d_%s_ResOnly %s%s%d_LSP%d_%s_ResOnly.txt " %(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
  #BoostedOnlyVeto
  if 'combined' in phase_space:
    combineCommands.append("combine -M AsymptoticLimits -n %s%s%d_LSP%d_%s_Combo %s%s%d_LSP%d_%s_Combo.txt " %(whichDString,signal,hino,LSP,dataMCString,whichDString,signal,hino,LSP,dataMCString))
  return combineCommands

if __name__ == '__main__':

  # Setup arguments
  parser = argparse.ArgumentParser(description='''\
  Combines resolved and boosted datacards.
  Requires boosted datacards to be in current working directory and 
  resolved datacards in one of the below directories:
  - resData/1DTChiHH_Data
  - resData/2DTChiHH_Data 
  - resData/1DT5HH_Data
  ''', formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('-s','--signal_model', required=True, help='Signal model: TChiHH-G or TChiHH or T5HH')
  parser.add_argument('-p','--mass_points', required=True, help='Signal mass points in following format: 500_100,500_1. Can also use "all"')
  parser.add_argument('-f','--fake_run', action="store_true", help='Does not run commands. Only print commands')
  parser.add_argument('-m','--only_merge', action="store_true", help='Do only merge datacards')
  parser.add_argument('-c','--only_combine', action="store_true", help='Do only combine')
  parser.add_argument('--phase_space', help='Phase space to process. Use following format: resolved,boosted,combined. Can also use "all"', default='all')
  args = parser.parse_args()
  # Set variables from arguments
  if args.signal_model == "TChiHH-G": 
    whichDString = "1D"
    signal = "TChiHH"
  elif args.signal_model == "TChiHH": 
    whichDString = "2D"
    signal = "TChiHH"
  elif args.signal_model == "T5HH":
    whichDString = "1D"
    signal = "T5HH"
  else:
    print("[Error] Undefined signal model: "+args.signalModel+". Exiting")
    sys.exit()
  # mass_points = [(NLSP, LSP)]
  mass_points = []
  if args.mass_points == "all":
    if args.signal_model == "TChiHH-G":
      mass_points = [[175+item*25, 1]for item in range(0, 54)]
    elif args.signal_model == "TChiHH":
      mass_points = getTChiHHMassPoints()
    elif args.signal_model == "T5HH":
      mass_points = [[1000+item*100,1] for item in range(0,16)]
  else:
    raw_mass_points = args.mass_points.split(',')
    mass_points = [item.split('_') for item in raw_mass_points]
  # phase_space = [resolved, boosted, combined]
  if args.phase_space == "all":
    phase_space = ['resolved', 'boosted', 'combined']
  else:
    phase_space = args.phase_space.split(',')

  print('Mass points: '+str(mass_points))

  t0 = time()

  # Merge datacard
  merge_commands = []
  for mass_point in mass_points:
    hino=mass_point[0]
    LSP=mass_point[1]
    if signal == "TChiHH":
      merge_commands.extend(makeMergeHiggsinoCommands(whichDString,signal,hino,LSP,"Data", phase_space))
    elif signal == "T5HH":
      merge_commands.extend(makeMergeGluinoCommands(whichDString,signal,hino,LSP,"Data", phase_space))
  if not args.only_combine:
    if args.fake_run: print('Commands to run:'+str(merge_commands))
    else: runCommands(merge_commands)

  # Run combine on datacards
  combine_commands = []
  for mass_point in mass_points:
    hino=mass_point[0]
    LSP=mass_point[1]
    combine_commands.extend(makeCombineCommands(whichDString,signal,hino,LSP,"Data", phase_space))
  if not args.only_merge:
    if args.fake_run: print('Commands to run:'+str(combine_commands))
    else: runCommands(combine_commands)

  print('\nProgram took %.0fm %.0fs.' % ((time()-t0)/60,(time()-t0)%60))
