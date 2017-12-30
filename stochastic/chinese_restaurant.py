"""Chinese restaurant process."""
import numpy as np

from stochastic.base import Sequence


class ChineseRestaurantProcess(Sequence):
    """Chinese restaurant process.

    A Chinese restaurant process consists of a sequence of arrivals of
    customers to a Chinese restaurant. Customers may be seated either at an
    occupied table or a new table, there being infinitely many customers
    and tables.

    The first customer sits at the first table. The n-th customer
    sits at a new table with probability 1/n, and at each already occupied
    table with probability t_k/n, where t_k is the number of customers
    already seated at table k. This is the canonical process with discount=0
    and strength=1.

    The generalized process gives the n-th customer a probability of
    (strength + T * discount) / (n - 1 + strength) to sit at a new table
    and a probability of (t_k - discount) / (n - 1 + strength) of sitting at
    table k. T is the number of occupied tables.
    """

    def __init__(self, discount=0, strength=1):
        self.discount = discount
        self.strength = strength

    @property
    def discount(self):
        """Discount parameter."""
        return self._discount

    @discount.setter
    def discount(self, value):
        self._check_number(value, "Discount")
        if value >= 1:
            raise ValueError("Discount value must be less than 1.")
        self._discount = value

    @property
    def strength(self):
        """Strength parameter."""
        return self._strength

    @strength.setter
    def strength(self, value):
        self._check_number(value, "Strength")
        if self.discount < 0:
            strength_positive = value / -self.discount <= 0
            strength_not_multiple = (value / -self.discount) % 1 != 0
            if strength_positive or strength_not_multiple:
                raise ValueError(
                    "When discount is negative, strength value must be equal "
                    "to a multiple of the discount value.")
        elif self.discount < 1:
            if value <= -self.discount:
                raise ValueError(
                    "When discount is between 0 and 1, strength value must be "
                    "greater than the negative of the discount")
        self._strength = value

    def __str__(self):
        return ("Chinese restaurant process with discount {d} "
                "and strength {s}").format(
                    d=str(self.discount),
                    s=str(self.strength)
        )

    def __repr__(self):
        return "ChineseRestaurantProcess(discount={d}, strength={s})".format(
            d=str(self.discount),
            s=str(self.strength)
        )

    def _sample_chinese_restaurant(self, n):
        """Generate a Chinese restaurant process with n customers."""
        self._check_increments(n)

        s = [[1]]
        num_tables = 1
        table_range = [0, 1]

        for k in range(2, n + 1):
            p = [1.0 * (len(s[t]) - self.discount) / (k - 1 + self.strength)
                 for t in table_range[:-1]]
            p.append(1.0 * (self.strength + num_tables * self.discount) /
                     (k - 1 + self.strength))
            table = np.random.choice(table_range, p=p)
            if table == num_tables:
                num_tables += 1
                table_range.append(num_tables)
                s.append([])
            s[table].append(k)

        return np.array(s)

    def sample(self, n):
        """Generate a Chinese restaurant process with n customers."""
        return self._sample_chinese_restaurant(n)
