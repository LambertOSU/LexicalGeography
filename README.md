# LexicalGeography

LexicalGeography is a tool for extracting location data from text.  It is heavily inspired by the geotext package, however it contains additional features that geotext does not.

The gazetteer is built with [GeoNames](http://www.geonames.org/) data.

The **lexigeo** class will identify the names of states (Admin 1) and counties (Admin 2) in addition to cities and countries.

LexicalGeography is under development.  I would like to optimize the gazetteer creation, as well as implement a method for predicting the "most likely location."

As of right now, the name "Franklin County, Virginia" will identify the state of Virginia, a city named Franklin, and the county name.  Since GeoNames provides all of the parent data, it can be used to predict the most likely single location.

**Required Files**

These files must be [downloaded from GeoNames](http://download.geonames.org/export/dump/).

- countryInfo.txt

- admin1CodesASCII.txt

- admin2Codes.txt

- cities1000.txt

Currently they are stored in a directory called ./01_location_data/ which is used in the class.  
