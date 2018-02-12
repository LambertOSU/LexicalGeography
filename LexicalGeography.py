# LexicalGeography is a tool for extracting location information from text.
# It is heavily inspired by the geotext package.  However, it identifies county
# and state names as well.

# This module is in development.

import pandas as pd
from collections import namedtuple
import nltk
from nltk.collocations import *

import time
#-------------------------------------------------------------------------------
def gazetteer_maker():

    # countries
    country_info = pd.read_table('./01_location_data/countryInfo.txt', skiprows=50)
    country_info = country_info[['Country','geonameid']]
    country_info['Country'] = country_info['Country'].str.lower()
    country_info.set_index('Country',inplace=True)
    countries = country_info.to_dict('index')

    # states
    columns = ['code', 'name' , 'ASCII name', 'geonameid']
    state_info = pd.read_table('./01_location_data/admin1CodesASCII.txt',header=None,names=columns)
    state_info = state_info[['geonameid', 'name']]
    state_info['name'] = state_info['name'].str.lower()
    state_info.set_index('name',inplace=True)
    states = state_info.to_dict('index')


    # counties
    columns = ['code', 'name' , 'ASCII name', 'geonameid']
    county_info = pd.read_table('./01_location_data/admin2Codes.txt',header=None,names=columns)
    county_info = county_info[['geonameid', 'name']]
    county_info['name'] = county_info['name'].str.lower()
    county_info.set_index('name',inplace=True)
    counties = county_info.to_dict('index')

    # cities
    columns = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude',
               'longitude','feature class','feature code', 'country code', 'cc2',
               'admin1code', 'admin2 code', 'admin3 code', 'admin4 code',
               'population', 'elevation', 'dem', 'timezone','modification date']

    city_info = pd.read_table('./01_location_data/cities1000.txt', header=None, names=columns)
    city_info = city_info[['geonameid', 'name']]
    city_info['name'] = city_info['name'].str.lower()
    city_info.set_index('name',inplace=True)
    cities = city_info.to_dict('index')

    gazetteer = namedtuple('gazetteer', 'countries states counties cities')
    return gazetteer(countries,states,counties,cities)

#-------------------------------------------------------------------------------
# class lexigeo
class lexigeo(object):

    def __init__(self, text, gaz):

        # define the gazetteer
        self.gaz = gaz

        # tokenize the text
        tknzr = nltk.tokenize.TweetTokenizer()
        tokens = tknzr.tokenize(text)

        # get the bigrams
        bigs = nltk.bigrams(tokens)

        # get the trigrams
        trigs = nltk.trigrams(tokens)

        # convert bigrams and trigrams into list of strings
        trig_list = [trig[0] + ' ' + trig[1] + ' ' + trig[2] for trig in trigs]
        big_list = [big[0] + ' ' + big[1] for big in bigs]

        # list of all possible samples
        samples = trig_list + big_list + tokens

        # identify names of countries
        self.countries = [name for name in samples
                          if name.lower() in self.gaz.countries]

        # identify names of states
        self.states = [name for name in samples
                       if name.lower() in self.gaz.states]

        # identify names of counties
        self.counties = [name for name in samples
                       if name.lower() in self.gaz.counties]

        # identify names of cities
        self.cities = [name for name in samples
                       if name.lower() in self.gaz.cities]


#-------------------------------------------------------------------------------
# Testing

def test_gazetteer_maker():
    g = gazetteer_maker()
    print(g.states)


def test_lexigeo():
    # header
    print('------------------------------------------------------------------')
    print('\nTesting LexicalGeography\n')

    # build the gazetteer and reprot build time
    print('------------------------------------------------------------------')
    print('\nBuilding gazetteer, this could take some time...\n')
    st = time.time()
    gaz = gazetteer_maker()
    print('\nGazetteer build time: ',time.time() - st,' seconds\n')

    # define text for testing
    text = "I live in Knoxville, Tennessee, but I am visiting Paris, France."
    print('Testing phrase: \"', text,'\"\n')

    # test the class
    st = time.time()
    lg = lexigeo(text,gaz)

    # report results
    print('------------------------------------------------------------------')
    print('Results')
    print('Countries: ',lg.countries)
    print('States (Admin 1): ',lg.states)
    print('Counties (Admin 2): ',lg.counties)
    print('Cities: ',lg.cities,'\n')
    print('Lookup time: ',time.time() - st,'\n')


if __name__ == '__main__':
    # test_gazetteer_maker()
    test_lexigeo()
    # g = gazetteer_maker()
