<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Currencies</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.currency-modal>Add</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Currency</th>
              <th scope="col">Buy for:</th>
              <th scope="col">Sell for:</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in currencies" :key="index">
              <td>{{ item.currency }}</td>
              <td>{{ item.buy_rate }}</td>
              <td>{{ item.sell_rate }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.currency-update-modal
                          @click="editCurrency(item)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteCurrency(item)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addCurrencyModal"
            id="currency-modal"
            title="Add a new currency"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-currency-group"
                    label="Currency:"
                    label-for="form-currency-input">
          <b-form-input id="form-currency-input"
                        type="text"
                        v-model="addCurrencyForm.currency"
                        required
                        placeholder="Enter currency">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-buy-for-group"
                      label="Buy price:"
                      label-for="form-buy-for-input">
            <b-form-input id="form-buy-for-input"
                          type="number"
                          step="0.0001"
                          v-model="addCurrencyForm.buy_rate"
                          required
                          placeholder="Enter buy price">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-sell-for-group"
                      label="Sell price:"
                      label-for="form-sell-for-input">
            <b-form-input id="form-sell-for-input"
                          type="number"
                          step="0.0001"
                          v-model="addCurrencyForm.sell_rate"
                          required
                          placeholder="Enter sell price">
            </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editCurrencyModal"
            id="currency-update-modal"
            title="Update"
            hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group id="form-buy-for-edit-group"
                        label="Buy price:"
                        label-for="form-buy-for-edit-input">
            <b-form-input id="form-buy-for-edit-input"
                          type="number"
                          step="0.0001"
                          v-model="editForm.buy_rate"
                          required
                          placeholder="Enter buy price">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-sell-for-edit-group"
                        label="Sell price:"
                        label-for="form-sell-for-edit-input">
            <b-form-input id="form-sell-for-edit-input"
                          type="number"
                          step="0.0001"
                          v-model="editForm.sell_rate"
                          required
                          placeholder="Enter sell price">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      currencies: [],
      addCurrencyForm: {
        currency: '',
        buy_rate: '',
        sell_rate: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        currency: '',
        buy_rate: '',
        sell_rate: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getCurrencies() {
      const path = 'http://localhost:5001/curr';
      axios.get(path)
        .then((res) => {
          this.currencies = res.data.currencies;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addCurrency(payload) {
      const path = `http://localhost:5001/curr/${payload.currency}`;
      axios.post(path, payload)
        .then(() => {
          this.getCurrencies();
          this.message = 'Currency added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getCurrencies();
        });
    },
    initForm() {
      this.addCurrencyForm.currency = '';
      this.addCurrencyForm.buy_rate = '';
      this.addCurrencyForm.sell_rate = '';
      this.editForm.currency = '';
      this.editForm.buy_rate = '';
      this.editForm.sell_rate = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addCurrencyModal.hide();

      const payload = {
        currency: this.addCurrencyForm.currency,
        buy_rate: this.addCurrencyForm.buy_rate,
        sell_rate: this.addCurrencyForm.sell_rate,

      };
      this.addCurrency(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addCurrencyModal.hide();
      this.initForm();
    },
    editCurrency(currency) {
      this.editForm = currency;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCurrencyModal.hide();
      const payload = {
        currency: this.editForm.currency,
        buy_rate: this.editForm.buy_rate,
        sell_rate: this.editForm.sell_rate,
      };
      this.updateCurrency(payload, this.editForm.currency); // ????
    },
    updateCurrency(payload, currName) {
      const path = `http://localhost:5001/curr/${currName}`;
      axios.put(path, payload)
        .then(() => {
          this.getCurrencies();
          this.message = 'Currency updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCurrencies();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCurrencyModal.hide();
      this.initForm();
      this.getCurrencies();
    },
    removeСurrency(currName) {
      const path = `http://localhost:5001/curr/${currName}`;
      axios.delete(path)
        .then(() => {
          this.getCurrencies();
          this.message = 'Currency removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCurrencies();
        });
    },
    onDeleteCurrency(item) {
      this.removeCurrency(item.currency);
    },
  },
  created() {
    this.getCurrencies();
  },
};
</script>
