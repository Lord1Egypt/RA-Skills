import { describe, expect, it } from "vitest";
import {
  Redactor,
  isValidLuhn,
  isValidNhs,
  isValidNi,
  isValidTokenMap,
  reinstate,
  selfCheck,
} from "@pharmatools/redacta";

const clinical = () => new Redactor(["clinical"]);
const general = () => new Redactor(["general"]);
const both = () => new Redactor(["clinical", "general"]);

describe("validators", () => {
  it("accepts a valid NHS number and rejects an invalid one", () => {
    expect(isValidNhs("9434765919")).toBe(true);
    expect(isValidNhs("9434765918")).toBe(false);
    expect(isValidNhs("1111111111")).toBe(false);
  });

  it("applies NI prefix rules", () => {
    expect(isValidNi("AB")).toBe(true);
    expect(isValidNi("BG")).toBe(false); // forbidden pair
    expect(isValidNi("DA")).toBe(false); // bad first letter
    expect(isValidNi("AO")).toBe(false); // bad second letter
  });

  it("validates Luhn card numbers", () => {
    expect(isValidLuhn("4111111111111111")).toBe(true);
    expect(isValidLuhn("4111111111111112")).toBe(false);
  });
});

describe("clinical mode", () => {
  it("redacts a valid NHS number but not an invalid 10-digit number", () => {
    const r = clinical();
    expect(r.redactText("NHS Number: 943 476 5919").text).toContain("[NHS_NUMBER_1]");
    const r2 = clinical();
    expect(r2.redactText("ref 123 456 7890").text).toContain("123 456 7890");
  });

  it("redacts DOB but preserves appointment dates", () => {
    const r = clinical();
    const { text } = r.redactText(
      "DOB: 14/03/1952. Your next appointment is on 15 March 2026."
    );
    expect(text).toContain("[DATE_OF_BIRTH_1]");
    expect(text).toContain("15 March 2026");
  });

  it("redacts NI numbers, postcodes, emails and UK phones", () => {
    const r = clinical();
    const { text } = r.redactText(
      "NI: AB 12 34 56 C, Leeds LS6 3PJ, jo@example.com, tel 0113 278 4532"
    );
    expect(text).toContain("[NI_NUMBER_1]");
    expect(text).toContain("[POSTCODE_1]");
    expect(text).toContain("[EMAIL_1]");
    expect(text).toContain("[PHONE_1]");
  });

  it("redacts keyword-anchored MRN and SSN", () => {
    const r = clinical();
    const { text } = r.redactText("Hospital Number: RXH-2847561, SSN: 123-45-6789");
    expect(text).toContain("[MRN_1]");
    expect(text).toContain("[SSN_1]");
  });

  it("gives the same value the same token everywhere", () => {
    const r = clinical();
    const a = r.redactText("Contact jo@example.com").text;
    const b = r.redactText("Email jo@example.com again").text;
    expect(a).toContain("[EMAIL_1]");
    expect(b).toContain("[EMAIL_1]");
  });

  it("does not redact general-only patterns", () => {
    const r = clinical();
    const input = "Visit https://example.com from 192.168.1.1";
    expect(r.redactText(input).text).toBe(input);
  });
});

describe("general mode", () => {
  it("redacts URLs, IPs and vehicle regs", () => {
    const r = general();
    const { text } = r.redactText(
      "See https://example.com/page from 192.168.1.1, car AB12 CDE"
    );
    expect(text).toContain("[URL_1]");
    expect(text).toContain("[IP_ADDRESS_1]");
    expect(text).toContain("[VEHICLE_REG_1]");
  });

  it("redacts Luhn-valid card numbers but not invalid ones", () => {
    const r = general();
    const { text } = r.redactText("Card 4111 1111 1111 1111, order 4111111111111112");
    expect(text).toContain("[CARD_NUMBER_1]");
    expect(text).toContain("4111111111111112");
  });

  it("redacts IBANs and keyword-anchored account numbers", () => {
    const r = general();
    const { text } = r.redactText(
      "IBAN GB29 NWBK 6016 1331 9268 19, Member ID: ZX-99812"
    );
    expect(text).toContain("[IBAN_1]");
    expect(text).toContain("[ACCOUNT_NUMBER_1]");
  });
});

describe("keyword-anchored names", () => {
  it("redacts a courtesy-titled patient name including the title", () => {
    const r = clinical();
    const { text } = r.redactText("Dear Mrs Patricia Hartley,");
    expect(text).toContain("Dear [PATIENT_NAME_1]");
    expect(text).not.toContain("Patricia");
    expect(text).not.toContain("Mrs");
  });

  it("redacts a salutation name with no title", () => {
    const r = clinical();
    expect(r.redactText("Dear Patricia Hartley,").text).toContain("Dear [PATIENT_NAME_1]");
  });

  it("redacts labelled names but keeps the label", () => {
    const r = clinical();
    const { text } = r.redactText("Patient: John Smith\nName - Jane Doe");
    expect(text).toContain("Patient: [PATIENT_NAME_1]");
    expect(text).toContain("Name - [PATIENT_NAME_2]");
  });

  it("PRESERVES clinician names carrying a clinical title", () => {
    const r = clinical();
    const input = "under the care of Dr Sarah Chen and Consultant James Wright";
    const { text } = r.redactText(input);
    expect(text).toBe(input); // nothing redacted
  });

  it("does not redact a clinician introduced by 'Dear Dr ...'", () => {
    const r = clinical();
    const { text } = r.redactText("Dear Dr Chen,");
    expect(text).toBe("Dear Dr Chen,");
  });

  it("gives the same patient the same name token across notes", () => {
    const r = clinical();
    const a = r.redactText("Dear Mrs Patricia Hartley").text;
    const b = r.redactText("Patient: Patricia Hartley").text;
    expect(a).toContain("[PATIENT_NAME_1]");
    expect(b).toContain("[PATIENT_NAME_1]");
  });
});

describe("relative and carer names", () => {
  it("redacts a relative's name but keeps the relationship word", () => {
    const r = clinical();
    const { text } = r.redactText("Her daughter Sarah visits daily.");
    expect(text).toContain("daughter [RELATIVE_NAME_1]");
    expect(text).not.toContain("Sarah");
  });

  it("redacts next-of-kin and carer names", () => {
    const r = clinical();
    const { text } = r.redactText("NOK: John Hartley. Carer Maria Lopez attends.");
    expect(text).toContain("[RELATIVE_NAME_1]");
    expect(text).toContain("[RELATIVE_NAME_2]");
    expect(text).not.toContain("John Hartley");
    expect(text).not.toContain("Maria Lopez");
  });

  it("does not fire on a relationship word with no following name", () => {
    const r = clinical();
    const input = "The patient has a daughter and two sons.";
    expect(r.redactText(input).text).toBe(input);
  });

  it("does not over-capture trailing lowercase words after a relative name", () => {
    const r = clinical();
    const { text } = r.redactText("Her daughter Sarah is the main contact.");
    expect(text).toBe("Her daughter [RELATIVE_NAME_1] is the main contact.");
    expect(r.tokenMap["[RELATIVE_NAME_1]"]).toBe("Sarah");
  });

  it("does not over-capture after a labelled patient name", () => {
    const r = clinical();
    const { text } = r.redactText("Patient: John is doing well.");
    expect(text).toBe("Patient: [PATIENT_NAME_1] is doing well.");
    expect(r.tokenMap["[PATIENT_NAME_1]"]).toBe("John");
  });
});

describe("self-check", () => {
  it("flags an identifier that survived redaction", () => {
    const findings = selfCheck("Contact 07700 900123 or visit https://example.com");
    const labels = findings.map((f) => f.label);
    expect(labels).toContain("long number (10+ digits)");
    expect(labels).toContain("URL");
  });

  it("ignores Redacta's own tokens and clean text", () => {
    expect(selfCheck("DOB: [DATE_OF_BIRTH_1], NHS: [NHS_NUMBER_1]")).toHaveLength(0);
    expect(selfCheck("The quick brown fox.")).toHaveLength(0);
  });

  it("confirms a real redaction leaves no residual identifiers", () => {
    const r = both();
    const { text } = r.redactText(
      "NHS Number: 943 476 5919, email p.hartley@example.com"
    );
    expect(selfCheck(text)).toHaveLength(0);
  });
});

describe("re-identification", () => {
  it("restores original values from a token map", () => {
    const map = {
      "[NHS_NUMBER_1]": "943 476 5919",
      "[PATIENT_NAME_1]": "Patricia Hartley",
    };
    const { text, changed } = reinstate(
      "Dear [PATIENT_NAME_1], your NHS number is [NHS_NUMBER_1].",
      map
    );
    expect(text).toBe("Dear Patricia Hartley, your NHS number is 943 476 5919.");
    expect(changed).toBe(true);
  });

  it("round-trips: redact then reinstate returns the original", () => {
    const original =
      "Dear Mrs Patricia Hartley, NHS Number: 943 476 5919, email p.hartley@example.com";
    const r = new Redactor(["clinical", "general"]);
    const redacted = r.redactText(original).text;
    expect(reinstate(redacted, r.tokenMap).text).toBe(original);
  });

  it("does not confuse [NAME_1] with [NAME_10]", () => {
    const map = { "[PATIENT_NAME_1]": "Anna", "[PATIENT_NAME_10]": "Zoe" };
    expect(reinstate("[PATIENT_NAME_10] and [PATIENT_NAME_1]", map).text).toBe(
      "Zoe and Anna"
    );
  });

  it("reports no change when there are no tokens", () => {
    expect(reinstate("nothing here", { "[EMAIL_1]": "x@y.com" }).changed).toBe(false);
  });

  it("validates token maps", () => {
    expect(isValidTokenMap({ "[NHS_NUMBER_1]": "943 476 5919" })).toBe(true);
    expect(isValidTokenMap({})).toBe(false);
    expect(isValidTokenMap({ foo: "bar" })).toBe(false);
    expect(isValidTokenMap({ "[NHS_NUMBER_1]": 123 })).toBe(false);
    expect(isValidTokenMap(null)).toBe(false);
    expect(isValidTokenMap([])).toBe(false);
  });
});

describe("combined mode and reporting", () => {
  it("handles the full sample letter", () => {
    const r = both();
    const { text, changed } = r.redactText(
      "Dear Mrs Patricia Hartley, DOB: 14/03/1952, NHS Number: 943 476 5919. " +
        "Address: 14 Oakfield Road, Leeds LS6 3PJ. Tel: 0113 278 4532. " +
        "Portal: https://myhealth.example.com"
    );
    expect(changed).toBe(true);
    expect(text).toContain("[DATE_OF_BIRTH_1]");
    expect(text).toContain("[NHS_NUMBER_1]");
    expect(text).toContain("[POSTCODE_1]");
    expect(text).toContain("[PHONE_1]");
    expect(text).toContain("[URL_1]");
    const report = r.report;
    expect(report.NHS_NUMBER).toBe(1);
    expect(report.URL).toBe(1);
  });

  it("exposes a token map for re-identification", () => {
    const r = both();
    r.redactText("NHS Number: 943 476 5919");
    expect(r.tokenMap["[NHS_NUMBER_1]"]).toBe("943 476 5919");
  });

  it("reports unchanged text correctly", () => {
    const r = both();
    const { changed } = r.redactText("The quick brown fox.");
    expect(changed).toBe(false);
    expect(Object.keys(r.report)).toHaveLength(0);
  });
});
