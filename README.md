This is intended as a repository of helpful python functions for theorycrafting in new world.


If you have suggestions or ideas for how it could be improved, open an issue or submit a pull request.




Ask if you want to use it for a commercial project.
Give credit if you use parts of this repository.

Some parts of this wouldn't have been possible without reverse engineering help from the nwdb discord, particularly Xyo and jesspacito, who helped with gs-based damage and finding a formula for crit chance that doesn't rely on simulation.
Also thanks to MorrolanTV,MixedNuts, CarpetMerchant, XR and others from the morrolan discord who helped with providing test data and who've done no small part in untangling the mess that is new world themselves.




## Usage Example:

```

gs=600
gsMultiplier(gs)*82*(1.2)*(1+levelscaling(60)+dmgstatScaling([5,35,5,5], [0,0.9,0.65,0]))*armorScaling(44,gs)
```

for a gs 600 musket with 35 dex and 5 int in light armor against a pve target with 44 armor.

Combat dummies in forts have 44 armor.

Note that the armor scaling function is currently outdated for use against players.


