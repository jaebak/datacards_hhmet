Datacards and script to merge and run datacards

Also at ```LCP@/uscms_data/d3/emacdona/WorkingArea/CombinedHiggs/forGithub/CMSSW_10_2_13/src/HHplusMET/datacards```

1. Copy all needed datacards to one folder, such as datacards.
2. cd the the folder and run combineAndRunDatacardsHiggsino.py, where below are some examples
 ```../combineAndRunDatacardsHiggsino.py --signal_model TChiHH-G --mass_points all --phase_space all```
 ```../combineAndRunDatacardsHiggsino.py --signal_model TChiHH --mass_points all --phase_space all```
 ```../combineAndRunDatacardsHiggsino.py --signal_model T5HH --mass_points all --phase_space all```
