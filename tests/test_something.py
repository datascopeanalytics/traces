import nose

import traces


def my_setup_function():
    pass


def my_teardown_function():
    pass


@nose.with_setup(my_setup_function, my_teardown_function)
def test_default_types():
    T = 0  # can be any key that's not in the time series
    assert traces.TimeSeries(default_type=int)[T] == 0
    assert traces.TimeSeries(default_type=float)[T] == 0.0
    assert traces.TimeSeries(default_type=list)[T] == []
    assert traces.TimeSeries(default_type=dict)[T] == {}
    assert traces.TimeSeries(default_type=set)[T] == set()


def test_compact():

    # make a v. simple time series
    ts = traces.TimeSeries()
    ts[0] = 42

    # set a future time to the same value, with compact=True
    ts.set(1, 42, compact=True)

    # should still only keep the t=0 measurement
    assert ts.n_measurements() == 1
    assert ts[0.5] == 42

    # now set a future value to a different value
    ts.set(1, 43, compact=True)

    # it should have the new measurement and a later time should
    # return the latest measurement
    assert ts.n_measurements() == 2
    assert ts[2] == 43


def test_remove():

    # v. simple time series
    ts = traces.TimeSeries()
    ts[0] = 42
    ts[1] = 43

    # asser that trying to delete a non-existent entry raises a
    # KeyError
    try:
        del ts[2]
    except KeyError:
        pass

    # now delete the measurement at t=1
    del ts[1]

    # now there should only be one measurement and the value of the
    # time series at a later time should be back at the original value
    assert ts.n_measurements() == 1
    assert ts[2] == 42