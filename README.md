# SpeedChecker

SpeedChecker is a tool for comparing your network bandwidth with that of a given postcode or partial postcode area e.g. ('SW' or 'SW6' or 'SW6 4DT') against Ofcom's [Connected Nations Reports](https://www.ofcom.org.uk/research-and-data/multi-sector-research/infrastructure-research/connected-nations-2016/downloads).
SpeedChecker comes 'preloaded' with data from 2016.

### Tech

SpeedChecker uses some open source projects to work properly:

* [Django](https://www.djangoproject.com/) - (v2.0.3) Python framework for web apps
* [ChartJS](http://www.chartjs.org/) - JS based responsive charts
* [Materialize CSS](http://materializecss.com/) - responsive front-end framework based on Material Design
* [pyspeedtest](https://github.com/fopina/pyspeedtest) - (v1.2.7) package to test network bandwidth using Speedtest.net servers
* [pandas](https://pandas.pydata.org/) (v0.22) package for fast data processing.
* [numpy](http://www.numpy.org/) (v1.14.2) package for scientific computing.
* [jQuery](https://jquery.com/) - for many reasons..

### Installation

SpeedChecker requires Python 3.6 or above to run.

Install the dependencies and start the server.

```sh
$ git clone https://github.com/Georgerowberry/SpeedChecker.git
$ cd SpeedChecker
$ pip3 install -r requirements.txt
$ python Checker/collate_data.py   (this may take a few minutes)
$ python manage.py runserver [port]
```
The server will be running on http://127.0.0.1:8000/ by defult

### Updating the Dataset

SpeedChecker comes with a script to write CSV files from Ofcom's [Connected Nations Report](https://www.ofcom.org.uk/research-and-data/multi-sector-research/infrastructure-research/connected-nations-2016/downloads) into the sqlite database.

To add new data to the database:

1) Add the new files into 'Speedchecker/Data/' folder.
2) ```sh
    $ cd SpeedChecker/Checker
    $ python collate_data.py
    ```

### Author
George Rowberry



