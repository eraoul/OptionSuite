import unittest
import csvData
import Queue as queue
import datetime
import pytz

class TestCSVHandler(unittest.TestCase):

    # Used to set up the unittest class
    def setUp(self):
        # Create CsvData class object
        self.dataProvider = 'iVolatility'
        self.directory = '/Users/msantoro/PycharmProjects/Backtester/sampleData'
        self.filename = 'aapl_sample_ivolatility.csv'
        self.eventQueue = queue.Queue()
        self.chunkSize = 1822
        self.csvObj = csvData.CsvData(self.directory, self.filename, self.dataProvider, self.eventQueue, self.chunkSize)

    def testGetOptionChain(self):
        # Get option chain for the first time/date from CSV.
        self.csvObj.getOptionChain()

        # Get event from the queue.
        event = self.eventQueue.get()
        data = event.getData()

        # Check that we got the right number of rows from the csv.
        self.assertEqual(len(data), 1822)

        # Get the first object of type put/call and do some basic checks.
        firstOption = data[0]

        # Check that we're able to get underlying ticker symbol.
        underlyingTicker = firstOption.getUnderlyingTicker()
        self.assertEqual(underlyingTicker, 'AAPL')

        # Check that we got the right option type.
        optionType = firstOption.getOptionType()
        self.assertEqual(optionType, 'CALL')

        # Check that we're able to get the correct date / time.
        curDateTime = firstOption.getDateTime()
        local = pytz.timezone('US/Eastern')
        dateTime = datetime.datetime.strptime('8/7/14', "%m/%d/%y")
        dateTime = local.localize(dateTime, is_dst=None)
        dateTime = dateTime.astimezone(pytz.utc)
        self.assertEqual(curDateTime, dateTime)

        # Get option chain for the second date/time from CSV.
        self.csvObj.getOptionChain()

        # Get event from the queue.
        event = self.eventQueue.get()
        data = event.getData()

        # Get the first object of type put/call and do some basic checks.
        firstOption = data[0]

        # Check that we're able to get underlying ticker symbol.
        underlyingTicker = firstOption.getUnderlyingTicker()
        self.assertEqual(underlyingTicker, 'SPY')

        # Check that we got the right option type.
        optionType = firstOption.getOptionType()
        self.assertEqual(optionType, 'CALL')

        # Check that we're able to get the correct date / time.
        curDateTime = firstOption.getDateTime()
        local = pytz.timezone('US/Eastern')
        dateTime = datetime.datetime.strptime('8/8/14', "%m/%d/%y")
        dateTime = local.localize(dateTime, is_dst=None)
        dateTime = dateTime.astimezone(pytz.utc)
        self.assertEqual(curDateTime, dateTime)

        # Try to get one more option chain -- this should result in an error.
        returnVal = self.csvObj.getOptionChain()

        # Check return value.
        self.assertEqual(returnVal, False)

if __name__ == '__main__':
    unittest.main()

