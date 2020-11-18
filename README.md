# ANTEATR-PARADE
This repo contains the most recent version of ANTEATR. ANTEATR-PARADE simulates the expansion and deformation of both the CME axis and cross section as the result of magnetic and drag forces. The main component is the function 'getAT' that is designed to be called by external functions. If PARADE.py is executed via 'python PARADE.py' then it will run the example at the very bottom of the code. The commented out portion at the bottom executes the simulations with different forces included/excluded as was done for the first PARADE paper. The options to toggle these forces on and off remain in the code but are not likely of use in most situations.

## Inputs
ANTEATR-PARADE requires two input vectors to run. The first contains all the parameters related to the CME and the background solar wind (referred to as invec in the code) and the second contains the satellite parameters (referred to as satParams).

The first input vector, invec, should contain in order (with units in []):
1. CME latitude [deg]
2. CME longitude [deg]
3. CME orientation [deg] 
4. CME radial velocity [km/s]
5. CME mass [1e15 g]
5. CME full angular width [deg]
7. CME cross section angular width [deg]
8. CME shape ratio delta_Ax [unitless]
9. CME shape ratio delta_CS [unitless]
10. CME shape ratio delta_CA [unitless]
11. CME front initial radial distance [Rs]
12. Ratio of CME B to SW B
13. Solar wind number density at L1 [cm^-3]
14. Solar wind velocity at L1 [km/s]
15. Solar wind magnetic field at L1 [nT]
16. Solar wind drag coefficient [unitless]
17. Flux rope tau parameter
18. Flux rope C parameter

The second input vector, satParmas, should contain:
1. Satellite latitude [deg]
2. Satellite longitude [deg]
3. Satellite distance [Rs]
4. Satellite orbital speed [deg/sec]

The main function, getAT, can also be passed a pair of scaling parameters fscales=[f1,f2], which are the parameters presented in the second PARADE paper and control whether the initial velcity decomposition is more convective-like or self-similar-like.

## Outputs
ANTEATR-PARADE returns four outputs - called outs, Elon, vs, and estDur in the example. Elon is the longitude of the satellite at the time of impact, which will not be the same as the initial value if it has an orbit and is useful for any models following ANTEATR-PARADE that calculate in situ properties. vs is an array with the individual components of the velocity at the time of impact ([vFront, vEdge, vBulk, vCSrad, vCSperp, vAxrad, vAxperp]). estDur is an estimate of the duration including the continued effects of expansion.

outs is a large array containing time profiles of different parameters, which can be used to generate figures. outs[i] is an array of a given output where i corresponds to:
0: Time [days]
1: CME nose distance [Rs]
2: Velocities [km/s] - this is an array of one vector for each time step with the order as listed above
3: CME full angular width [deg]
4: CME cross section angular width [deg]
5: CME shape ratio delta_Ax [unitless]
6: CME shape ratio delta_CS [unitless]
7: CME shape ratio delta_CA [unitless]
8: CME magnetic field strength [G]
9: Flux rope C parameter

Note that the magnetic field strength corresponds to the parameter B0 used in our magnetic field model, which then can be used to calculate the toroidal and poloidal field strengths given deltaCS, C, and tau.
