"""ML-ENSEMBLE

Place holder for more rigorous tests.

"""
import numpy as np
from mlens.ensemble import (SequentialEnsemble,
                            SuperLearner,
                            BlendEnsemble,
                            Subsemble)

from mlens.utils.dummy import (Data,
                               PREPROCESSING,
                               ESTIMATORS,
                               ECM,
                               LayerGenerator)


FOLDS = 3
LEN = 24
WIDTH = 2
MOD = 2

data = Data('stack', False, True, FOLDS)
X, y = data.get_data((LEN, WIDTH), MOD)


lc_s = LayerGenerator().get_layer_container('stack', False, True)
lc_b = LayerGenerator().get_layer_container('blend', False, False)
lc_u = LayerGenerator().get_layer_container('subset', False, False)


def test_fit():
    """[Sequential] Test multilayer fitting."""

    S = lc_s.fit(X, y, -1)[-1]
    B = lc_b.fit(S, y, -1)[-1]
    U = lc_u.fit(B, y, -1)[-1]

    ens = SequentialEnsemble()
    ens.add('stack', ESTIMATORS, PREPROCESSING)
    ens.add('blend', ECM)
    ens.add('subset', ECM)

    out = ens.layers.fit(X, y, -1)[-1]

    np.testing.assert_array_equal(U, out)


def test_predict():
    """[Sequential] Test multilayer prediction."""

    S = lc_s.predict(X, y)
    B = lc_b.predict(S, y)
    U = lc_u.predict(B, y)

    ens = SequentialEnsemble()
    ens.add('stack', ESTIMATORS, PREPROCESSING)
    ens.add('blend', ECM)
    ens.add('subset', ECM)

    out = ens.fit(X, y).predict(X)

    np.testing.assert_array_equal(U, out)


def test_equivalence_super_learner():
    """[Sequential] Test ensemble equivalence with SuperLearner."""

    ens = SuperLearner()
    seq = SequentialEnsemble()

    ens.add(ECM)
    seq.add('stack', ECM)

    F = ens.fit(X, y).predict(X)
    P = seq.fit(X, y).predict(X)

    np.testing.assert_array_equal(P, F)


def test_equivalence_blend():
    """[Sequential] Test ensemble equivalence with BlendEnsemble."""

    ens = BlendEnsemble()
    seq = SequentialEnsemble()

    ens.add(ECM)
    seq.add('blend', ECM)

    F = ens.fit(X, y).predict(X)
    P = seq.fit(X, y).predict(X)

    np.testing.assert_array_equal(P, F)


def test_equivalence_subsemble():
    """[Sequential] Test ensemble equivalence with Subsemble."""

    ens = Subsemble()
    seq = SequentialEnsemble()

    ens.add(ECM)
    seq.add('subset', ECM)

    F = ens.fit(X, y).predict(X)
    P = seq.fit(X, y).predict(X)

    np.testing.assert_array_equal(P, F)
