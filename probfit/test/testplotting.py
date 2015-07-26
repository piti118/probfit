import matplotlib
matplotlib.use('Agg', warn=False)
import os
from os.path import dirname, join
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison
from matplotlib.testing.compare import compare_images
from iminuit import Minuit
from probfit.plotting import draw_pdf, draw_compare_hist
from probfit.pdf import gaussian, linear
from probfit.funcutil import rename
from probfit.functor import Extended, AddPdfNorm, AddPdf
from probfit.costfunc import UnbinnedLH, BinnedLH, BinnedChi2, Chi2Regression, \
                             SimultaneousFit

class image_comparison:
    def __init__(self, baseline):
        baselineimage = join(dirname(__file__), 'baseline', baseline)
        actualimage = join(os.getcwd(), 'actual', baseline)

        self.baseline = baseline
        self.baselineimage = baselineimage
        self.actualimage = actualimage

        try:
            os.makedirs(dirname(actualimage))
        except OSError:
            pass

    def setup(self):
        from matplotlib import rcParams, rcdefaults
        #use('Agg', warn=False)  # use Agg backend for these tests

        # These settings *must* be hardcoded for running the comparison
        # tests and are not necessarily the default values as specified in
        # rcsetup.py
        rcdefaults()  # Start with all defaults
        rcParams['font.family'] = 'Bitstream Vera Sans'
        rcParams['text.hinting'] = False
        rcParams['text.hinting_factor'] = 8
        rcParams['text.antialiased'] = False
        rcParams['lines.antialiased'] = False


    def test(self):
        # compare_images
        x = compare_images(self.baselineimage, self.actualimage, 1.0)
        if x is not None:
            print x
            assert x is None


    def __call__(self, f):
        def tmp():
            self.setup()
            f()
            plt.savefig(self.actualimage)
            plt.close()
            return self.test()
        tmp.__name__ = f.__name__
        return tmp


@image_comparison('draw_pdf.png')
def test_draw_pdf():
    plt.figure()
    f = gaussian
    draw_pdf(f, {'mean':1., 'sigma':2.}, bound=(-10, 10))


@image_comparison('draw_pdf_linear.png')
def test_draw_pdf_linear():
    plt.figure()
    f = linear
    draw_pdf(f, {'m':1., 'c':2.}, bound=(-10, 10))


