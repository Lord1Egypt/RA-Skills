# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Fixed Income — Structured Products
====================================
Weighted average life (WAL), CPR/SMM conversion, PSA prepayment model,
mortgage cash flow projection, and average life sensitivity to prepayment
speed.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class PrepaymentModel:
    """CPR/SMM conversion and PSA prepayment speed calculations.

    Provides static methods for prepayment rate conversions and the
    PSA benchmark prepayment model.
    """

    @staticmethod
    def smm_from_cpr(cpr: float) -> float:
        """Convert CPR (annual) to SMM (monthly).

        Parameters
        ----------
        cpr : float
            Conditional Prepayment Rate as a decimal (e.g., 0.06 = 6%).

        Returns
        -------
        float
            SMM = 1 - (1 - CPR)^(1/12)
        """
        return float(1.0 - (1.0 - cpr) ** (1.0 / 12.0))

    @staticmethod
    def cpr_from_smm(smm: float) -> float:
        """Convert SMM (monthly) to CPR (annual).

        Parameters
        ----------
        smm : float
            Single Monthly Mortality rate as a decimal.

        Returns
        -------
        float
            CPR = 1 - (1 - SMM)^12
        """
        return float(1.0 - (1.0 - smm) ** 12.0)

    @staticmethod
    def psa_cpr(month: int, psa_speed: float = 100.0) -> float:
        """Compute the CPR for a given month under the PSA model.

        100% PSA ramps linearly from 0% CPR to 6% CPR over the first
        30 months, then plateaus at 6% CPR. Other PSA speeds scale
        proportionally.

        Parameters
        ----------
        month : int
            Loan age in months (1-indexed).
        psa_speed : float, optional
            PSA speed as a percentage (e.g., 150 = 150% PSA). Default is 100.

        Returns
        -------
        float
            CPR for the given month as a decimal.
        """
        if month <= 0:
            raise ValueError("Month must be >= 1.")
        psa_factor = psa_speed / 100.0
        if month <= 30:
            base_cpr = 0.06 * (month / 30.0)
        else:
            base_cpr = 0.06
        return float(base_cpr * psa_factor)

    @staticmethod
    def psa_smm(month: int, psa_speed: float = 100.0) -> float:
        """Compute SMM for a given month under the PSA model.

        Parameters
        ----------
        month : int
            Loan age in months.
        psa_speed : float, optional
            PSA speed as a percentage. Default is 100.

        Returns
        -------
        float
            SMM for the given month.
        """
        cpr = PrepaymentModel.psa_cpr(month, psa_speed)
        return PrepaymentModel.smm_from_cpr(cpr)

    @staticmethod
    def psa_cpr_schedule(
        n_months: int,
        psa_speed: float = 100.0,
    ) -> np.ndarray:
        """Generate a full CPR schedule under the PSA model.

        Parameters
        ----------
        n_months : int
            Number of months in the schedule.
        psa_speed : float, optional
            PSA speed. Default is 100.

        Returns
        -------
        np.ndarray
            Array of CPR values for months 1 through n_months.
        """
        months = np.arange(1, n_months + 1)
        cprs = np.where(
            months <= 30,
            0.06 * (months / 30.0) * (psa_speed / 100.0),
            0.06 * (psa_speed / 100.0),
        )
        return cprs


class MortgageCashFlow:
    """Project monthly cash flows for a mortgage pass-through security.

    Parameters
    ----------
    original_balance : float
        Original pool balance.
    mortgage_rate : float
        Annual mortgage rate as a decimal (e.g., 0.06 = 6%).
    original_term : int
        Original loan term in months (e.g., 360 for 30-year).
    current_age : int, optional
        Current age of the pool in months. Default is 0 (new pool).
    passthrough_rate : float or None, optional
        Annual pass-through rate to investors. If None, uses mortgage_rate.
        The difference is the servicing fee.
    """

    def __init__(
        self,
        original_balance: float,
        mortgage_rate: float,
        original_term: int = 360,
        current_age: int = 0,
        passthrough_rate: float | None = None,
    ):
        self.original_balance = original_balance
        self.mortgage_rate = mortgage_rate
        self.monthly_rate = mortgage_rate / 12.0
        self.original_term = original_term
        self.current_age = current_age
        self.remaining_term = original_term - current_age
        self.passthrough_rate = passthrough_rate if passthrough_rate is not None else mortgage_rate
        self.monthly_passthrough = self.passthrough_rate / 12.0

    def _scheduled_payment(self, balance: float, remaining_months: int) -> float:
        """Compute the scheduled monthly mortgage payment.

        Parameters
        ----------
        balance : float
            Current outstanding balance.
        remaining_months : int
            Months remaining on the loan.

        Returns
        -------
        float
            Level monthly payment (principal + interest).
        """
        r = self.monthly_rate
        if r == 0:
            return balance / remaining_months
        return float(balance * r * (1.0 + r) ** remaining_months /
                      ((1.0 + r) ** remaining_months - 1.0))

    def project(self, psa_speed: float = 100.0) -> dict:
        """Project monthly cash flows under a given PSA speed.

        Parameters
        ----------
        psa_speed : float, optional
            PSA prepayment speed. Default is 100.

        Returns
        -------
        dict
            Dictionary with arrays:
            - 'month': month numbers
            - 'beginning_balance': balance at start of month
            - 'scheduled_payment': total scheduled payment
            - 'interest': interest portion of scheduled payment
            - 'scheduled_principal': scheduled principal repayment
            - 'prepayment': prepayment amount
            - 'total_principal': scheduled + prepaid principal
            - 'total_cash_flow': interest + total principal (to investor)
            - 'ending_balance': balance at end of month
            - 'smm': single monthly mortality rate
        """
        n = self.remaining_term
        months = np.zeros(n, dtype=np.int64)
        beg_balance = np.zeros(n)
        sched_payment = np.zeros(n)
        interest = np.zeros(n)
        sched_principal = np.zeros(n)
        prepayment = np.zeros(n)
        total_principal = np.zeros(n)
        total_cf = np.zeros(n)
        end_balance = np.zeros(n)
        smm_arr = np.zeros(n)

        balance = self.original_balance

        for i in range(n):
            month_number = self.current_age + i + 1
            months[i] = month_number
            beg_balance[i] = balance

            remaining = n - i

            # Scheduled payment
            pmt = self._scheduled_payment(balance, remaining)
            sched_payment[i] = pmt

            # Interest
            int_payment = balance * self.monthly_rate
            interest[i] = int_payment

            # Scheduled principal
            sp = pmt - int_payment
            sched_principal[i] = sp

            # Prepayment (on balance after scheduled principal)
            smm = PrepaymentModel.psa_smm(month_number, psa_speed)
            smm_arr[i] = smm
            pp = (balance - sp) * smm
            prepayment[i] = pp

            # Totals
            tp = sp + pp
            total_principal[i] = tp

            # Cash flow to investor uses passthrough rate for interest
            investor_interest = balance * self.monthly_passthrough
            total_cf[i] = investor_interest + tp

            # Ending balance
            balance = balance - tp
            if balance < 0.01:
                balance = 0.0
            end_balance[i] = balance

            if balance == 0.0:
                # Truncate arrays
                months = months[: i + 1]
                beg_balance = beg_balance[: i + 1]
                sched_payment = sched_payment[: i + 1]
                interest = interest[: i + 1]
                sched_principal = sched_principal[: i + 1]
                prepayment = prepayment[: i + 1]
                total_principal = total_principal[: i + 1]
                total_cf = total_cf[: i + 1]
                end_balance = end_balance[: i + 1]
                smm_arr = smm_arr[: i + 1]
                break

        return {
            "month": months,
            "beginning_balance": beg_balance,
            "scheduled_payment": sched_payment,
            "interest": interest,
            "scheduled_principal": sched_principal,
            "prepayment": prepayment,
            "total_principal": total_principal,
            "total_cash_flow": total_cf,
            "ending_balance": end_balance,
            "smm": smm_arr,
        }


class StructuredAnalytics:
    """Weighted average life and sensitivity analysis for structured products."""

    @staticmethod
    def weighted_average_life(
        principal_payments: np.ndarray,
        months: np.ndarray,
    ) -> float:
        """Compute weighted average life (WAL) in years.

        Parameters
        ----------
        principal_payments : np.ndarray
            Array of total principal payments (scheduled + prepaid) per period.
        months : np.ndarray
            Array of month numbers corresponding to each payment.

        Returns
        -------
        float
            WAL = sum(t * Principal_t) / sum(Principal_t), converted to years.
        """
        total_principal = np.sum(principal_payments)
        if total_principal == 0:
            return 0.0
        # Convert months to years for the weighting
        years = months / 12.0
        return float(np.sum(years * principal_payments) / total_principal)

    @staticmethod
    def wal_sensitivity(
        original_balance: float,
        mortgage_rate: float,
        original_term: int,
        psa_speeds: np.ndarray,
        current_age: int = 0,
    ) -> dict:
        """Compute WAL across a range of PSA speeds.

        Parameters
        ----------
        original_balance : float
            Original pool balance.
        mortgage_rate : float
            Annual mortgage rate as a decimal.
        original_term : int
            Original loan term in months.
        psa_speeds : np.ndarray
            Array of PSA speeds to evaluate (e.g., [50, 100, 150, 200, 300]).
        current_age : int, optional
            Current pool age in months. Default is 0.

        Returns
        -------
        dict
            Dictionary with 'psa_speeds' and 'wal_years' arrays.
        """
        speeds = np.asarray(psa_speeds, dtype=np.float64)
        wals = np.zeros_like(speeds)

        for i, speed in enumerate(speeds):
            pool = MortgageCashFlow(
                original_balance=original_balance,
                mortgage_rate=mortgage_rate,
                original_term=original_term,
                current_age=current_age,
            )
            cf = pool.project(psa_speed=speed)
            wals[i] = StructuredAnalytics.weighted_average_life(
                cf["total_principal"], cf["month"]
            )

        return {
            "psa_speeds": speeds.tolist(),
            "wal_years": wals.tolist(),
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Structured products analysis
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Fixed Income Structured Products — Demo")
    print("=" * 60)

    # ----- CPR/SMM Conversion -----
    print("\n--- CPR/SMM Conversion ---")
    cpr = 0.06
    smm = PrepaymentModel.smm_from_cpr(cpr)
    cpr_back = PrepaymentModel.cpr_from_smm(smm)
    print(f"\n  CPR = {cpr*100:.2f}%")
    print(f"  SMM = {smm*100:.4f}%")
    print(f"  Round-trip CPR = {cpr_back*100:.2f}%")

    # ----- PSA Model -----
    print("\n--- PSA Prepayment Model ---")
    print(f"\n  {'Month':>6s}  {'100% PSA':>10s}  {'150% PSA':>10s}  {'200% PSA':>10s}")
    print(f"  {'-'*6}  {'-'*10}  {'-'*10}  {'-'*10}")
    for month in [1, 5, 10, 15, 20, 25, 30, 36, 60, 120]:
        cpr100 = PrepaymentModel.psa_cpr(month, 100)
        cpr150 = PrepaymentModel.psa_cpr(month, 150)
        cpr200 = PrepaymentModel.psa_cpr(month, 200)
        print(f"  {month:6d}  {cpr100*100:9.2f}%  {cpr150*100:9.2f}%  {cpr200*100:9.2f}%")

    # Verify worked example from SKILL.md: 150% PSA month 20
    cpr_ex = PrepaymentModel.psa_cpr(20, 150)
    smm_ex = PrepaymentModel.psa_smm(20, 150)
    print(f"\n  Worked example: 150% PSA, month 20")
    print(f"    CPR = {cpr_ex*100:.1f}%")
    print(f"    SMM = {smm_ex*100:.3f}%")

    # ----- Mortgage Cash Flow Projection -----
    print("\n--- Mortgage Cash Flow Projection ---")
    pool = MortgageCashFlow(
        original_balance=1_000_000.0,
        mortgage_rate=0.06,
        original_term=360,
        passthrough_rate=0.055,
    )
    cf = pool.project(psa_speed=150)

    # Show first 12 months and last 3 months
    print(f"\n  $1M Pool, 6.0% WAC, 5.5% pass-through, 150% PSA")
    print(f"  {'Month':>6s}  {'Beg Bal':>12s}  {'Interest':>10s}  {'Sched Prin':>12s}  {'Prepay':>10s}  {'End Bal':>12s}")
    print(f"  {'-'*6}  {'-'*12}  {'-'*10}  {'-'*12}  {'-'*10}  {'-'*12}")
    for i in list(range(min(12, len(cf["month"])))) + list(range(max(0, len(cf["month"]) - 3), len(cf["month"]))):
        if i == 12 and len(cf["month"]) > 15:
            print(f"  {'...':>6s}  {'...':>12s}  {'...':>10s}  {'...':>12s}  {'...':>10s}  {'...':>12s}")
        print(
            f"  {cf['month'][i]:6d}"
            f"  ${cf['beginning_balance'][i]:11,.2f}"
            f"  ${cf['interest'][i]:9,.2f}"
            f"  ${cf['scheduled_principal'][i]:11,.2f}"
            f"  ${cf['prepayment'][i]:9,.2f}"
            f"  ${cf['ending_balance'][i]:11,.2f}"
        )

    total_principal = np.sum(cf["total_principal"])
    total_interest = np.sum(cf["interest"])
    print(f"\n  Total principal returned: ${total_principal:,.2f}")
    print(f"  Total interest paid:     ${total_interest:,.2f}")
    print(f"  Pool life:               {len(cf['month'])} months ({len(cf['month'])/12:.1f} years)")

    # ----- Weighted Average Life -----
    print("\n--- Weighted Average Life ---")
    wal = StructuredAnalytics.weighted_average_life(
        cf["total_principal"], cf["month"]
    )
    print(f"\n  WAL at 150% PSA: {wal:.2f} years")

    # ----- WAL Sensitivity -----
    print("\n--- WAL Sensitivity to Prepayment Speed ---")
    speeds = np.array([0, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500])
    sensitivity = StructuredAnalytics.wal_sensitivity(
        original_balance=1_000_000.0,
        mortgage_rate=0.06,
        original_term=360,
        psa_speeds=speeds,
    )

    print(f"\n  {'PSA Speed':>10s}  {'WAL (years)':>12s}")
    print(f"  {'-'*10}  {'-'*12}")
    for speed, w in zip(sensitivity["psa_speeds"], sensitivity["wal_years"]):
        print(f"  {speed:9.0f}%  {w:11.2f}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)

def _check(failures: list, name: str, actual: float, expected: float, tol: float) -> None:
    """Record a verification check result."""
    ok = abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: actual={actual:.6g}, expected={expected:.6g}, tol={tol:.2g}")
    if not ok:
        failures.append(name)

def _verify() -> None:
    """Verify key outputs against the SKILL.md worked examples."""
    failures: list = []

    # SKILL.md Example 1: 150% PSA, month 20
    _check(failures, "Ex1 CPR (month 20, 150% PSA)", PrepaymentModel.psa_cpr(20, 150), 0.06, 1e-12)
    _check(failures, "Ex1 SMM (month 20, 150% PSA)", PrepaymentModel.psa_smm(20, 150), 0.00514, 1e-5)

    # CPR/SMM round trip
    smm = PrepaymentModel.smm_from_cpr(0.06)
    _check(failures, "CPR->SMM->CPR round trip", PrepaymentModel.cpr_from_smm(smm), 0.06, 1e-12)

    # PSA plateau: 100% PSA after month 30 is 6% CPR
    _check(failures, "100% PSA plateau", PrepaymentModel.psa_cpr(60, 100), 0.06, 1e-12)

    # WAL sensitivity is monotonically decreasing in PSA speed
    sens = StructuredAnalytics.wal_sensitivity(1_000_000.0, 0.06, 360,
                                               np.array([50.0, 150.0, 300.0]))
    wals = sens["wal_years"]
    _check(failures, "WAL decreases with faster prepayment",
           1.0 if wals[0] > wals[1] > wals[2] else 0.0, 1.0, 0)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: PrepaymentModel, MortgageCashFlow, StructuredAnalytics. "
            "For programmatic use, import this module (fixed_income_structured) instead of running it. "
            "Bare run executes a demo whose printed values match the SKILL.md worked examples; "
            "--verify asserts those values and exits nonzero on mismatch."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the verification checks against the SKILL.md worked-example values",
    )
    args = parser.parse_args()
    if args.verify:
        _verify()
    else:
        _demo()


if __name__ == "__main__":
    main()
