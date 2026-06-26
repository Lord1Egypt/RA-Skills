package com.example.model;

import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Example of Builder Pattern implementation.
 *
 * Use Builder Pattern when:
 * - Class has many parameters (4+)
 * - Some parameters are optional
 * - You want to ensure immutability
 * - You want to make object construction more readable
 */
public final class User {

    // All fields are final for immutability
    private final Long id;
    private final String email;
    private final String firstName;
    private final String lastName;
    private final String phoneNumber;
    private final Address address;
    private final boolean isActive;
    private final LocalDateTime createdAt;
    private final LocalDateTime updatedAt;

    /**
     * Private constructor - only accessible through Builder.
     */
    private User(Builder builder) {
        this.id = builder.id;
        this.email = builder.email;
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.phoneNumber = builder.phoneNumber;
        this.address = builder.address;
        this.isActive = builder.isActive;
        this.createdAt = builder.createdAt;
        this.updatedAt = builder.updatedAt;
    }

    /**
     * Static factory method to create a new Builder.
     */
    public static Builder builder() {
        return new Builder();
    }

    /**
     * Builder class for constructing User instances.
     */
    public static class Builder {
        // Required fields (no default values)
        private Long id;
        private String email;
        private String firstName;
        private String lastName;

        // Optional fields (with default values)
        private String phoneNumber;
        private Address address;
        private boolean isActive = true;
        private LocalDateTime createdAt = LocalDateTime.now();
        private LocalDateTime updatedAt = LocalDateTime.now();

        /**
         * Private constructor - use User.builder() instead.
         */
        private Builder() {
        }

        /**
         * Sets the user ID.
         *
         * @param id the user ID
         * @return this builder for method chaining
         */
        public Builder id(Long id) {
            this.id = id;
            return this;
        }

        /**
         * Sets the user email (required).
         *
         * @param email the user email
         * @return this builder for method chaining
         */
        public Builder email(String email) {
            this.email = email;
            return this;
        }

        /**
         * Sets the user first name (required).
         *
         * @param firstName the user first name
         * @return this builder for method chaining
         */
        public Builder firstName(String firstName) {
            this.firstName = firstName;
            return this;
        }

        /**
         * Sets the user last name (required).
         *
         * @param lastName the user last name
         * @return this builder for method chaining
         */
        public Builder lastName(String lastName) {
            this.lastName = lastName;
            return this;
        }

        /**
         * Sets the user phone number (optional).
         *
         * @param phoneNumber the user phone number
         * @return this builder for method chaining
         */
        public Builder phoneNumber(String phoneNumber) {
            this.phoneNumber = phoneNumber;
            return this;
        }

        /**
         * Sets the user address (optional).
         *
         * @param address the user address
         * @return this builder for method chaining
         */
        public Builder address(Address address) {
            this.address = address;
            return this;
        }

        /**
         * Sets whether the user is active (optional, defaults to true).
         *
         * @param isActive true if user is active
         * @return this builder for method chaining
         */
        public Builder isActive(boolean isActive) {
            this.isActive = isActive;
            return this;
        }

        /**
         * Sets the creation timestamp (optional, defaults to now).
         *
         * @param createdAt the creation timestamp
         * @return this builder for method chaining
         */
        public Builder createdAt(LocalDateTime createdAt) {
            this.createdAt = createdAt;
            return this;
        }

        /**
         * Sets the last update timestamp (optional, defaults to now).
         *
         * @param updatedAt the last update timestamp
         * @return this builder for method chaining
         */
        public Builder updatedAt(LocalDateTime updatedAt) {
            this.updatedAt = updatedAt;
            return this;
        }

        /**
         * Builds and returns the User instance.
         *
         * @return the constructed User
         * @throws IllegalStateException if required fields are missing
         */
        public User build() {
            validateRequiredFields();
            validateBusinessRules();
            return new User(this);
        }

        /**
         * Validates that all required fields are set.
         */
        private void validateRequiredFields() {
            if (email == null || email.trim().isEmpty()) {
                throw new IllegalStateException("Email is required");
            }
            if (firstName == null || firstName.trim().isEmpty()) {
                throw new IllegalStateException("First name is required");
            }
            if (lastName == null || lastName.trim().isEmpty()) {
                throw new IllegalStateException("Last name is required");
            }
        }

        /**
         * Validates business rules.
         */
        private void validateBusinessRules() {
            if (!isValidEmail(email)) {
                throw new IllegalStateException("Invalid email format: " + email);
            }
        }

        /**
         * Simple email validation.
         */
        private boolean isValidEmail(String email) {
            return email.contains("@") && email.contains(".");
        }
    }

    // Getters only (no setters - immutable)

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public Address getAddress() {
        return address;
    }

    public boolean isActive() {
        return isActive;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    /**
     * Returns full name.
     */
    public String getFullName() {
        return firstName + " " + lastName;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User user = (User) o;
        return Objects.equals(id, user.id) &&
               Objects.equals(email, user.email);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, email);
    }

    @Override
    public String toString() {
        return "User{" +
               "id=" + id +
               ", email='" + email + '\'' +
               ", firstName='" + firstName + '\'' +
               ", lastName='" + lastName + '\'' +
               ", isActive=" + isActive +
               '}';
    }
}

// Example usage:
class UserExample {
    public static void main(String[] args) {
        // Create user with required fields only
        User user1 = User.builder()
            .email("john@example.com")
            .firstName("John")
            .lastName("Doe")
            .build();

        // Create user with all fields
        User user2 = User.builder()
            .id(1L)
            .email("jane@example.com")
            .firstName("Jane")
            .lastName("Smith")
            .phoneNumber("555-1234")
            .address(new Address("123 Main St", "Springfield", "IL", "62701"))
            .isActive(true)
            .build();

        // Method chaining is clear and readable
        User user3 = User.builder()
            .email("bob@example.com")
            .firstName("Bob")
            .lastName("Johnson")
            .phoneNumber("555-5678")
            .build();
    }
}
