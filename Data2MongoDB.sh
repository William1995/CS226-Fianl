#!/bin/bash
for filename in Dataset/*.js; do

	find="Dataset/"
	find2='.js'
	replace=""
	cityname=${filename//$find/$replace}
	cityname=${cityname//$find2/$replace}
	mongo --eval "use $cityname"
	mongoimport --db $cityname --collection tweet <$filename

done