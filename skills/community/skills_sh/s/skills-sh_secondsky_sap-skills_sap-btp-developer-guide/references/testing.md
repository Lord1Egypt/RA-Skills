# SAP BTP Testing Reference

## Overview

Quality assurance requires comprehensive testing across multiple dimensions including UI, usability, performance, and unit testing.

## Testing Strategy

### Test Pyramid

```
        /\
       /  \     E2E/UI Tests (few, slow)
      /----\
     /      \   Integration Tests (some)
    /--------\
   /          \  Unit Tests (many, fast)
  /------------\
```

### Benefits of Unit Testing

- Detect issues fast
- Better maintainable code
- More understandable code
- CI/CD integration
- Regression prevention

## CAP Testing

### Jest Setup

```javascript
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@sap/cds-dk": "^7.0.0"
  }
}
```

### Unit Test Example

```javascript
// test/unit/catalog-service.test.js
const cds = require('@sap/cds');

describe('CatalogService', () => {
  let srv;

  beforeAll(async () => {
    srv = await cds.connect.to('CatalogService');
  });

  afterAll(async () => {
    await cds.disconnect();
  });

  describe('READ Books', () => {
    it('should return all books', async () => {
      const books = await srv.read('Books');
      expect(books).toBeDefined();
      expect(Array.isArray(books)).toBe(true);
    });

    it('should filter by title', async () => {
      const books = await srv.read('Books').where({ title: 'Test Book' });
      expect(books.length).toBeLessThanOrEqual(1);
    });
  });

  describe('CREATE Books', () => {
    it('should create a book', async () => {
      const book = await srv.create('Books', {
        title: 'New Book',
        stock: 10
      });
      expect(book.ID).toBeDefined();
      expect(book.title).toBe('New Book');
    });

    it('should reject invalid data', async () => {
      await expect(srv.create('Books', {}))
        .rejects.toThrow();
    });
  });
});
```

### Integration Test Example

```javascript
// test/integration/api.test.js
const cds = require('@sap/cds');
const { GET, POST, PATCH, DELETE } = cds.test(__dirname + '/..');

describe('API Integration', () => {
  it('GET /catalog/Books', async () => {
    const { status, data } = await GET('/catalog/Books');
    expect(status).toBe(200);
    expect(data.value).toBeDefined();
  });

  it('POST /catalog/Books', async () => {
    const { status, data } = await POST('/catalog/Books', {
      title: 'Test Book',
      stock: 5
    });
    expect(status).toBe(201);
    expect(data.ID).toBeDefined();
  });

  it('GET /catalog/Books/:id', async () => {
    const { data: created } = await POST('/catalog/Books', { title: 'Test' });
    const { status, data } = await GET(`/catalog/Books(${created.ID})`);
    expect(status).toBe(200);
    expect(data.title).toBe('Test');
  });
});
```

## SAPUI5 Testing

### QUnit Framework

**Best Practice**: Write small, focused tests

```javascript
// webapp/test/unit/model/formatter.js
sap.ui.define([
  "my/app/model/formatter"
], function(formatter) {
  "use strict";

  QUnit.module("formatter");

  QUnit.test("formatStatus", function(assert) {
    assert.strictEqual(
      formatter.formatStatus("OPEN"),
      "Open",
      "Status formatted correctly"
    );
  });

  QUnit.test("formatDate", function(assert) {
    const date = new Date("2024-01-15");
    assert.strictEqual(
      formatter.formatDate(date),
      "Jan 15, 2024",
      "Date formatted correctly"
    );
  });
});
```

### OPA5 Integration Tests

```javascript
// webapp/test/integration/pages/List.js
sap.ui.define([
  "sap/ui/test/Opa5",
  "sap/ui/test/actions/Press"
], function(Opa5, Press) {
  "use strict";

  Opa5.createPageObjects({
    onTheListPage: {
      actions: {
        iPressOnFirstItem: function() {
          return this.waitFor({
            controlType: "sap.m.ObjectListItem",
            success: function(aItems) {
              new Press().executeOn(aItems[0]);
            }
          });
        }
      },
      assertions: {
        iShouldSeeTheList: function() {
          return this.waitFor({
            id: "list",
            success: function() {
              Opa5.assert.ok(true, "List is visible");
            }
          });
        }
      }
    }
  });
});
```

### OPA5 Journey

```javascript
// webapp/test/integration/AllJourneys.js
sap.ui.define([
  "sap/ui/test/Opa5",
  "./pages/List",
  "./ListJourney"
], function(Opa5) {
  "use strict";

  Opa5.extendConfig({
    viewNamespace: "my.app.view.",
    autoWait: true
  });
});

// webapp/test/integration/ListJourney.js
sap.ui.define([
  "sap/ui/test/opaQunit"
], function(opaTest) {
  "use strict";

  QUnit.module("List Journey");

  opaTest("Should see the list", function(Given, When, Then) {
    Given.iStartMyApp();
    Then.onTheListPage.iShouldSeeTheList();
    Given.iTeardownMyApp();
  });

  opaTest("Should navigate to detail", function(Given, When, Then) {
    Given.iStartMyApp();
    When.onTheListPage.iPressOnFirstItem();
    Then.onTheDetailPage.iShouldSeeTheDetail();
    Given.iTeardownMyApp();
  });
});
```

## ABAP Testing

### ABAP Unit

```abap
CLASS ltcl_travel DEFINITION FINAL FOR TESTING
  DURATION SHORT
  RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    CLASS-DATA: mo_environment TYPE REF TO if_cds_test_environment.
    DATA: mo_cut TYPE REF TO zcl_travel_handler.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS test_validate_dates FOR TESTING.
    METHODS test_calculate_total FOR TESTING.
ENDCLASS.

CLASS ltcl_travel IMPLEMENTATION.

  METHOD class_setup.
    mo_environment = cl_cds_test_environment=>create(
      i_for_entity = 'ZI_TRAVEL'
    ).
  ENDMETHOD.

  METHOD class_teardown.
    mo_environment->destroy( ).
  ENDMETHOD.

  METHOD setup.
    mo_environment->clear_doubles( ).
    mo_cut = NEW #( ).
  ENDMETHOD.

  METHOD test_validate_dates.
    " Given
    DATA(lv_begin) = cl_abap_context_info=>get_system_date( ).
    DATA(lv_end) = lv_begin + 7.

    " When
    DATA(lv_valid) = mo_cut->validate_dates(
      iv_begin = lv_begin
      iv_end = lv_end
    ).

    " Then
    cl_abap_unit_assert=>assert_true( lv_valid ).
  ENDMETHOD.

  METHOD test_calculate_total.
    " Given
    DATA(lv_booking_fee) = CONV decfloat16( '50.00' ).
    DATA(lv_price) = CONV decfloat16( '500.00' ).

    " When
    DATA(lv_total) = mo_cut->calculate_total(
      iv_booking_fee = lv_booking_fee
      iv_price = lv_price
    ).

    " Then
    cl_abap_unit_assert=>assert_equals(
      exp = '550.00'
      act = lv_total
    ).
  ENDMETHOD.

ENDCLASS.
```

### CDS Test Double Framework

```abap
" Create test doubles for CDS entities
DATA(lo_env) = cl_cds_test_environment=>create(
  i_for_entity = 'ZI_TRAVEL'
).

" Insert test data
DATA: lt_travel TYPE TABLE OF ztravel.
lt_travel = VALUE #(
  ( travel_uuid = cl_uuid_factory=>create_uuid_c32( )
    travel_id = '1'
    customer_id = 'CUST001'
    begin_date = '20240101'
    end_date = '20240108' )
).
lo_env->insert_test_data( lt_travel ).

" Run tests...

" Clear after tests
lo_env->clear_doubles( ).
```

## Test Automation

### CI/CD Integration

```yaml
# .pipeline/config.yml
stages:
  Additional Unit Tests:
    npmExecuteScripts: true
    npmScripts:
      - test

  Integration Tests:
    npmExecuteScripts: true
    npmScripts:
      - test:integration

  UI Tests:
    karmaExecuteTests: true
```

### Code Coverage

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

## Best Practices

### Unit Tests
1. Test one thing at a time
2. Use descriptive names
3. Follow AAA pattern (Arrange, Act, Assert)
4. Mock external dependencies
5. Keep tests fast

### Integration Tests
1. Test real interactions
2. Use test data that represents production
3. Clean up after tests
4. Test error paths

### UI Tests
1. Test user journeys
2. Use page objects pattern
3. Keep tests maintainable
4. Test accessibility

## Source Documentation

- Testing: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/performing-ui-usability-and-unit-tests-50a7c7d.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/performing-ui-usability-and-unit-tests-50a7c7d.md)
- SAPUI5 Testing: [https://sapui5.hana.ondemand.com/#/topic/291c9121e6044ab381e0b51716f97f52](https://sapui5.hana.ondemand.com/#/topic/291c9121e6044ab381e0b51716f97f52)
- CAP Testing: [https://cap.cloud.sap/docs/node.js/cds-test](https://cap.cloud.sap/docs/node.js/cds-test)
