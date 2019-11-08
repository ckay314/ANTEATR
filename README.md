# ANTEATR
This repo contains two files- funcANTEATR.py and makeensemble.py.  funcANTEATR is the basic ANTEATR code in a function form that can be called by the ensemble script.  makeensemble sets up the ensembles and runs ANTEATR.  The simulation is run as "python makeensemble.py"

## funcANTEATR
This file contains the function getAT, which take an input array of simulation properties and separately the initial radius of the CME (in solar radii).  The input vector should contain in order (with units in []):
1. Earth latitude at the start of the simulation [deg]
2. Earth longitude at the start of the simulation [deg]
3. CME latitude [deg]
4. CME longitude [deg]
5. CME radial velocity [km/s]
6. CME mass [1e15 g]
7. CME angular width [deg]
8. CME shape ratio A [unitless]
9. CME shape ratio B [unitless]
10. Solar wind velocity at L1 [km/s]
11. Solar wind number density at L1 [cm^-3]

The time of impact is actually calculated for a radial distance corresponding to L1 (213 solar radii).  This can be switched to 1 AU by changing the 213s to 215s if desired.  

The first while loop moves the CME from the starting distance to 213, while including the effects of 1D drag on the CME velocity.  After it reaches 213 solar radial, the second while loop continues to propagate it forward, but begins checking to see if the synthetic satellite/Earth is within the volume of the CME.  Once impact occurs it returns the travel time and the current radial CME velocity.  

The distance from the CME's toroidal axis is calculated in the second while look.  As the CME approaches impact this will decrease.  If no impact occurs then it should begin increasing before it reaches a distance less than the cross-sectional width.  When the distance increases we stop the simulation and return a transit time and speed of 9999 and -9999 to signify no impact.

Line 82 currently sets there to be no rotation/orbit of the Earth.  For real predictions this should be commented out as the orbit is important for precise predictions, but we do not include it in the ensemble study to focus on the effects from the variation in other parameters.

## makeensemble
This is just a wrapper script for repeatedly calling funcANTEATR to generate the ensembles used in the Kay, Mays, and Verbeke (2019) paper.  The two lambda functions at the top scale the CME velocity and angular width based on the mass.  We define the control input vector then loop through different scale (mass) CMEs and vary each input parameter one at a time.  The results are just printed to a screen because I got lazy and just use "python makeensemble.py > output.dat" rather than actually printing to file within the code. 